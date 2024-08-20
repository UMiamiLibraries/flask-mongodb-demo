from flask import Blueprint

research_assistant = Blueprint('research_assistant', __name__)

from . import routes