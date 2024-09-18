# research_assistant/routes.py

from flask import render_template, request, jsonify, redirect, url_for, flash
from flask import current_app
from . import research_assistant
from .forms import ScholarSearchForm, ResearchProjectForm
from .scholar_search import search_google_scholar
from .models import ResearchProject
from ..finding_aid_analyzer.models import FindingAidAnalysis
from ..finding_aid_analyzer.utils import analyze_finding_aid

@research_assistant.route('/', methods=['GET', 'POST'])
def index():
    form = ScholarSearchForm()
    projects = ResearchProject.get_all()
    return render_template('research_assistant/index.html', form=form, projects=projects)

@research_assistant.route('/project/new', methods=['GET', 'POST'])
def new_project():
    form = ResearchProjectForm()
    if form.validate_on_submit():
        project_id = ResearchProject.create(form.title.data, form.description.data, form.education_level.data)
        flash('Research project created successfully!', 'success')
        return redirect(url_for('research_assistant.view_project', project_id=project_id))
    return render_template('research_assistant/project_form.html', form=form, title="New Research Project")

@research_assistant.route('/project/<project_id>')
def view_project(project_id):
    project = ResearchProject.get_by_id(project_id)
    if project:
        search_form = ScholarSearchForm()
        search_results = ResearchProject.get_search_results(project_id)
        finding_aids = ResearchProject.get_finding_aids(project_id)

        for finding_aid in finding_aids:
            analysis = FindingAidAnalysis.get_by_file_id(finding_aid['_id'])
            if analysis:
                finding_aid['extracted_text_pages'] = analysis.extracted_text_pages
            else:
                finding_aid['extracted_text_pages'] = []

        return render_template('research_assistant/project_detail.html',
                               project=project,
                               search_results=search_results,
                               finding_aids=finding_aids,
                               form=search_form,
                               education_level=project.education_level)
    flash('Project not found', 'error')
    return redirect(url_for('research_assistant.index'))


@research_assistant.route('/project/<project_id>/edit', methods=['GET', 'POST'])
def edit_project(project_id):
    project = ResearchProject.get_by_id(project_id)
    if not project:
        flash('Project not found', 'error')
        return redirect(url_for('research_assistant.index'))

    form = ResearchProjectForm(obj=project)
    if form.validate_on_submit():
        if ResearchProject.update(project_id, form.title.data, form.description.data, form.education_level.data):
            flash('Research project updated successfully!', 'success')
            return redirect(url_for('research_assistant.view_project', project_id=project_id))
        flash('Failed to update project', 'error')
    return render_template('research_assistant/project_form.html', form=form, title="Edit Research Project")


@research_assistant.route('/project/<project_id>/delete', methods=['POST'])
def delete_project(project_id):
    if ResearchProject.delete(project_id):
        flash('Research project deleted successfully!', 'success')
    else:
        flash('Failed to delete project', 'error')
    return redirect(url_for('research_assistant.index'))

@research_assistant.route('/project/<project_id>/search', methods=['POST'])
def project_search(project_id):
    form = ScholarSearchForm()
    if form.validate_on_submit():
        query = form.query.data
        results = search_google_scholar(query)
        for result in results:
            ResearchProject.add_search_result(project_id, result)
        flash(f'Added {len(results)} search results to the project', 'success')
    return redirect(url_for('research_assistant.view_project', project_id=project_id))

@research_assistant.route('/project/<project_id>/remove_finding_aid', methods=['POST'])
def remove_finding_aid(project_id):
    finding_aid_id = request.json.get('finding_aid_id')
    if not finding_aid_id:
        return jsonify({'success': False, 'message': 'Finding aid ID is required'}), 400

    # Remove the finding aid from the project
    if ResearchProject.remove_finding_aid(project_id, finding_aid_id):
        # Remove the project from the finding aid's analysis
        analyses = FindingAidAnalysis.get_by_project(project_id)
        for analysis in analyses:
            if analysis.file_id == finding_aid_id:
                FindingAidAnalysis.remove_from_project(str(analysis._id), project_id)
        return jsonify({'success': True, 'message': 'Finding aid removed from the project'})
    else:
        return jsonify({'success': False, 'message': 'Failed to remove finding aid from the project'}), 500


@research_assistant.route('/project/<project_id>/analyze', methods=['POST'])
def analyze_text(project_id):
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