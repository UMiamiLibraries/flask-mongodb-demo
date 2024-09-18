# finding_aid_analyzer/forms.py

from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import SelectField
from wtforms.validators import DataRequired

class FindingAidUploadForm(FlaskForm):
    file = FileField('Upload Finding Aid (PDF)', validators=[
        FileRequired(),
        FileAllowed(['pdf'], 'PDF files only!')
    ])
    education_level = SelectField('Education Level', choices=[
        ('undergraduate', 'Undergraduate'),
        ('graduate', 'Graduate'),
        ('doctoral', 'Doctoral')
    ])
    project = SelectField('Associated Research Project', validators=[DataRequired()], coerce=str)

    def __init__(self, *args, project_choices=None, **kwargs):
        super(FindingAidUploadForm, self).__init__(*args, **kwargs)
        if project_choices:
            self.project.choices = project_choices