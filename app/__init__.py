import os
from flask import Flask
from flask_wtf.csrf import CSRFProtect
from pymongo import MongoClient
from .config import config

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY', 'fallback-secret-key')
    app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, config['faa_pdf_upload_folder'])
    app.config['MAX_CONTENT_LENGTH'] = eval(config['faa_pdf_max_content_length'])

    # Set OpenAI API key
    app.config['OPENAI_API_KEY'] = config['faa_openai_api_key']


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

    from .finding_aid_analyzer import finding_aid_analyzer as finding_aid_analyzer_blueprint
    app.register_blueprint(finding_aid_analyzer_blueprint, url_prefix='/finding-aid-analyzer')

    from .routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app