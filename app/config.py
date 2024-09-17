import os

config = {
    "faa_openai_api_key": os.environ.get("FAA_OPENAI_API_KEY"),
    "faa_pdf_upload_folder": os.environ.get("FAA_PDF_UPLOAD_FOLDER", "static/findingaids"),
    "faa_pdf_max_content_length": os.environ.get("FAA_PDF_MAX_CONTENT_LENGTH", "10 * 1024 * 1024"),
}