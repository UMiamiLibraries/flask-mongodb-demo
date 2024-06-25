from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired, NumberRange

class BookForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    author = StringField('Author', validators=[DataRequired()])
    isbn = StringField('ISBN', validators=[DataRequired()])
    published_year = IntegerField('Published Year', validators=[DataRequired(), NumberRange(min=1000, max=9999)])
    genre = StringField('Genre', validators=[DataRequired()])
    submit = SubmitField('Submit')