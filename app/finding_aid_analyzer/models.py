# models.py
from bson import ObjectId
from datetime import datetime

class FindingAidAnalysis:
    def __init__(self, file_id, summary, research_topics, education_level):
        self.file_id = file_id
        self.summary = summary
        self.research_topics = research_topics
        self.education_level = education_level
        self.created_at = datetime.utcnow()

    def to_dict(self):
        return {
            "file_id": self.file_id,
            "summary": self.summary,
            "research_topics": self.research_topics,
            "education_level": self.education_level,
            "created_at": self.created_at
        }

    @staticmethod
    def from_dict(data):
        analysis = FindingAidAnalysis(
            data['file_id'],
            data['summary'],
            data['research_topics'],
            data['education_level']
        )
        analysis.created_at = data['created_at']
        return analysis