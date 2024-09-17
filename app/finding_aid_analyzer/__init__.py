# __init__.py
from flask import Blueprint

finding_aid_analyzer = Blueprint('finding_aid_analyzer', __name__)

from . import routes