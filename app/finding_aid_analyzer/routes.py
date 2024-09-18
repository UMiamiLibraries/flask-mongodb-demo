# finding_aid_analyzer/routes.py

import os
from datetime import datetime
from flask import render_template, request, current_app, flash, redirect, url_for, jsonify
from werkzeug.utils import secure_filename
from . import finding_aid_analyzer
from .forms import FindingAidUploadForm
from .models import FindingAidAnalysis
from .utils import analyze_finding_aid, allowed_file, extract_text_from_pdf
from ..research_assistant.models import ResearchProject
from bson import ObjectId

@finding_aid_analyzer.route('/', methods=['GET', 'POST'])
def upload_finding_aid():
    """
    Handle the upload of a finding aid PDF file.
    """
    projects = ResearchProject.get_all()
    project_choices = [(str(p._id), p.title) for p in projects]

    form = FindingAidUploadForm(project_choices=project_choices)

    if form.validate_on_submit():
        file = form.file.data
        education_level = form.education_level.data
        project_id = form.project.data

        if file and allowed_file(file.filename):
            try:
                filename = secure_filename(file.filename)
                file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)

                file_id = current_app.db.finding_aids.insert_one({
                    "filename": filename,
                    "path": file_path,
                    "upload_date": datetime.utcnow()
                }).inserted_id

                extracted_text_pages = extract_text_from_pdf(file_path)

                analysis_id = FindingAidAnalysis.create(
                    str(file_id),
                    education_level,
                    project_id,
                    extracted_text_pages
                )

                ResearchProject.add_finding_aid(project_id, str(file_id))

                flash('Finding aid uploaded and text extracted successfully!', 'success')
                return redirect(url_for('research_assistant.view_project', project_id=project_id))
            except Exception as e:
                current_app.logger.error(f"Error processing finding aid: {str(e)}")
                flash('An error occurred while processing the finding aid.', 'error')
                return redirect(url_for('finding_aid_analyzer.upload_finding_aid'))
        else:
            flash('Invalid file type. Please upload a PDF file.', 'error')

    return render_template('finding_aid_analyzer/upload.html', form=form)

@finding_aid_analyzer.route('/analyze', methods=['POST'])
def analyze_text():
    """
    Analyze selected text from a finding aid.
    """
    data = request.json
    analysis_id = data.get('analysis_id')
    selected_text = data.get('selected_text')
    education_level = data.get('education_level')

    if not all([analysis_id, selected_text, education_level]):
        return jsonify({'error': 'Missing required data'}), 400

    try:
        summary, research_topics = analyze_finding_aid(selected_text, education_level)
        FindingAidAnalysis.update_analysis(analysis_id, summary, research_topics)
        return jsonify({'summary': summary, 'research_topics': research_topics})
    except Exception as e:
        current_app.logger.error(f"Error analyzing text: {str(e)}")
        return jsonify({'error': 'An error occurred while analyzing the text'}), 500