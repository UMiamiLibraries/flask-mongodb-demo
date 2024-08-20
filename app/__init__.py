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

    # Ensure output directory exists
    output_dir = os.path.join(app.root_path, 'static', 'output')
    os.makedirs(output_dir, exist_ok=True)

    from .books import books as books_blueprint
    app.register_blueprint(books_blueprint, url_prefix='/books')

    from .image_processor import image_processor as image_processor_blueprint
    app.register_blueprint(image_processor_blueprint, url_prefix='/image-processor')

    from .research_assistant import research_assistant as research_assistant_blueprint
    app.register_blueprint(research_assistant_blueprint, url_prefix='/research-assistant')

    from .routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app