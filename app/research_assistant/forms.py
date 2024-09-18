# research_assistant/forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, SelectField
from wtforms.validators import DataRequired

class ScholarSearchForm(FlaskForm):
    query = StringField('Search Query', validators=[DataRequired()])
    submit = SubmitField('Search')

class ResearchProjectForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    education_level = SelectField('Education Level', choices=[
        ('undergraduate', 'Undergraduate'),
        ('graduate', 'Graduate'),
        ('doctoral', 'Doctoral')
    ], validators=[DataRequired()])
    submit = SubmitField('Save')