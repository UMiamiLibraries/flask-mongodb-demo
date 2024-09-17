from flask import render_template, request, jsonify, redirect, url_for, flash
from . import research_assistant
from .forms import ScholarSearchForm, ResearchProjectForm
from .scholar_search import search_google_scholar
from .models import ResearchProject

@research_assistant.route('/', methods=['GET', 'POST'])
def index():
    form = ScholarSearchForm()
    projects = ResearchProject.get_all()
    return render_template('research_assistant/index.html', form=form, projects=projects)

@research_assistant.route('/project/new', methods=['GET', 'POST'])
def new_project():
    form = ResearchProjectForm()
    if form.validate_on_submit():
        project_id = ResearchProject.create(form.title.data, form.description.data)
        flash('Research project created successfully!', 'success')
        return redirect(url_for('research_assistant.view_project', project_id=project_id))
    return render_template('research_assistant/project_form.html', form=form, title="New Research Project")

@research_assistant.route('/project/<project_id>')
def view_project(project_id):
    project = ResearchProject.get_by_id(project_id)
    if project:
        search_form = ScholarSearchForm()  # Add this line
        search_results = ResearchProject.get_search_results(project_id)
        return render_template('research_assistant/project_detail.html', project=project, search_results=search_results, form=search_form)  # Update this line
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
        if ResearchProject.update(project_id, form.title.data, form.description.data):
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