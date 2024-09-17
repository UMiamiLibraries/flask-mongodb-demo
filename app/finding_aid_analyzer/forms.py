# forms.py
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import SelectField

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