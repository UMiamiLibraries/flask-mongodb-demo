from flask import Blueprint

image_processor = Blueprint('image_processor', __name__)

from . import routes