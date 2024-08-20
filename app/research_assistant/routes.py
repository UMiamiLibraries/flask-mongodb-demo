from flask import render_template, request, jsonify
from . import research_assistant
from .forms import ScholarSearchForm
from .scholar_search import search_google_scholar

@research_assistant.route('/', methods=['GET', 'POST'])
def index():
    form = ScholarSearchForm()
    results = []
    if form.validate_on_submit():
        query = form.query.data
        results = search_google_scholar(query)
    return render_template('research_assistant/index.html', form=form, results=results)