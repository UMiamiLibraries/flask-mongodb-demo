from flask import render_template, Blueprint
from datetime import datetime

main = Blueprint('main', __name__)

@main.route('/')
def home():
    return render_template('home.html')

@main.context_processor
def inject_year():
    return {'current_year': datetime.now().year}