# routes.py
import os
from datetime import datetime
from flask import render_template, request, current_app, flash, redirect, url_for
from werkzeug.utils import secure_filename
from . import finding_aid_analyzer
from .forms import FindingAidUploadForm
from .models import FindingAidAnalysis
from .utils import analyze_finding_aid, allowed_file
from bson import ObjectId

@finding_aid_analyzer.route('/', methods=['GET', 'POST'])
def upload_finding_aid():
    form = FindingAidUploadForm()
    if form.validate_on_submit():
        file = form.file.data
        education_level = form.education_level.data

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            # Store file info in MongoDB
            file_id = current_app.db.finding_aids.insert_one({
                "filename": filename,
                "path": file_path,
                "upload_date": datetime.utcnow()
            }).inserted_id

            # Analyze the finding aid
            summary, research_topics = analyze_finding_aid(file_path, education_level)

            # Store analysis results
            analysis = FindingAidAnalysis(file_id, summary, research_topics, education_level)
            current_app.db.analyses.insert_one(analysis.to_dict())

            return redirect(url_for('finding_aid_analyzer.analysis_results', file_id=file_id))

    return render_template('finding_aid_analyzer/upload.html', form=form)

@finding_aid_analyzer.route('/results/<file_id>')
def analysis_results(file_id):
    analysis = current_app.db.analyses.find_one({"file_id": ObjectId(file_id)})
    if analysis:
        return render_template('finding_aid_analyzer/results.html', analysis=analysis)
    flash('Analysis not found', 'error')
    return redirect(url_for('finding_aid_analyzer.upload_finding_aid'))
