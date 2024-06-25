import os
from flask import Flask
from flask_wtf.csrf import CSRFProtect
from pymongo import MongoClient

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY', 'fallback-secret-key')
    csrf = CSRFProtect(app)

    client = MongoClient('mongodb://mongo:27017/')
    app.db = client.library_db

    from .books import books as books_blueprint
    app.register_blueprint(books_blueprint, url_prefix='/books')

    from .routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app