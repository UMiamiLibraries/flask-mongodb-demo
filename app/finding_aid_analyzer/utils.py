# finding_aid_analyzer/utils.py
import os
from openai import OpenAI
from flask import current_app
from werkzeug.utils import secure_filename
from functools import lru_cache
import PyPDF2


ALLOWED_EXTENSIONS = {'pdf'}

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_text_from_pdf(file_path):
    extracted_pages = []
    with open(file_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        for page in pdf_reader.pages:
            extracted_pages.append(page.extract_text())
    return extracted_pages


@lru_cache(maxsize=100)
def analyze_finding_aid(text_to_analyze, education_level):
    attempts = 0
    max_attempts = 2

    client = OpenAI(api_key=current_app.config['OPENAI_API_KEY'])

    while attempts < max_attempts:
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": f"You are an AI assistant analyzing a finding aid for a {education_level} student. Provide a summary of the finding aid and suggest 5 research topics based on its content. Start the research topics with 'Research Topics:' on a new line."},
                    {"role": "user", "content": f"Analyze this finding aid for a {education_level} student: {text_to_analyze}"}
                ],
                temperature=0.7,
                max_tokens=1000
            )

            content = response.choices[0].message.content

            parts = content.split("Research Topics:", 1)
            if len(parts) == 2:
                summary, topics = parts
                research_topics = [topic.strip() for topic in topics.strip().split("\n") if topic.strip()]
            else:
                summary = content
                research_topics = []

            return summary.strip(), research_topics
        except Exception as e:
            attempts += 1
            if attempts == max_attempts:
                raise Exception(f"Failed to analyze finding aid after {max_attempts} attempts: {str(e)}")

    return "Failed to analyze the finding aid.", []
