# finding_aid_analyzer/models.py
from bson import ObjectId
from datetime import datetime
from flask import current_app

class FindingAidAnalysis:
    def __init__(self, file_id, summary=None, research_topics=None, education_level=None, project_ids=None, extracted_text_pages=None):
        self.file_id = file_id
        self.summary = summary
        self.research_topics = research_topics
        self.education_level = education_level
        self.project_ids = project_ids or []
        self.extracted_text_pages = extracted_text_pages or []
        self.created_at = datetime.utcnow()

    def to_dict(self):
        return {
            "file_id": self.file_id,
            "summary": self.summary,
            "research_topics": self.research_topics,
            "education_level": self.education_level,
            "project_ids": self.project_ids,
            "extracted_text_pages": self.extracted_text_pages,
            "created_at": self.created_at
        }

    @staticmethod
    def from_dict(data):
        analysis = FindingAidAnalysis(
            data['file_id'],
            data.get('summary'),
            data.get('research_topics'),
            data.get('education_level'),
            data.get('project_ids', []),
            data.get('extracted_text_pages', [])
        )
        analysis.created_at = data['created_at']
        return analysis


    @staticmethod
    def create(file_id, education_level, project_id, extracted_text_pages):
        analysis = FindingAidAnalysis(file_id, education_level=education_level, project_ids=[project_id], extracted_text_pages=extracted_text_pages)
        result = current_app.db.analyses.insert_one(analysis.to_dict())
        return str(result.inserted_id)

    @staticmethod
    def get_by_id(analysis_id):
        analysis = current_app.db.analyses.find_one({"_id": ObjectId(analysis_id)})
        if analysis:
            return FindingAidAnalysis.from_dict(analysis)
        return None

    @staticmethod
    def update_analysis(analysis_id, summary, research_topics):
        result = current_app.db.analyses.update_one(
            {"_id": ObjectId(analysis_id)},
            {"$set": {"summary": summary, "research_topics": research_topics}}
        )
        return result.modified_count > 0

    @staticmethod
    def add_to_project(analysis_id, project_id):
        result = current_app.db.analyses.update_one(
            {"_id": ObjectId(analysis_id)},
            {"$addToSet": {"project_ids": project_id}}
        )
        return result.modified_count > 0

    @staticmethod
    def remove_from_project(analysis_id, project_id):
        result = current_app.db.analyses.update_one(
            {"_id": ObjectId(analysis_id)},
            {"$pull": {"project_ids": project_id}}
        )
        return result.modified_count > 0

    @staticmethod
    def get_by_project(project_id):
        analyses = current_app.db.analyses.find({"project_ids": project_id})
        return [FindingAidAnalysis.from_dict(analysis) for analysis in analyses]

    @staticmethod
    def delete(analysis_id):
        result = current_app.db.analyses.delete_one({"_id": ObjectId(analysis_id)})
        return result.deleted_count > 0

    @staticmethod
    def get_by_file_id(file_id):
        analysis = current_app.db.analyses.find_one({"file_id": str(file_id)})
        if analysis:
            return FindingAidAnalysis.from_dict(analysis)
        return None