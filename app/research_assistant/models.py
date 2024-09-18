# research_assistant/models.py

from bson import ObjectId
from flask import current_app

class ResearchProject:
    def __init__(self, title, description, _id=None, finding_aid_ids=None, education_level=None):
        self.title = title
        self.description = description
        self._id = _id
        self.finding_aid_ids = finding_aid_ids or []
        self.education_level = education_level

    @staticmethod
    def create(title, description, education_level):
        project = {
            'title': title,
            'description': description,
            'finding_aid_ids': [],
            'education_level': education_level
        }
        result = current_app.db.research_projects.insert_one(project)
        return str(result.inserted_id)

    @staticmethod
    def get_all():
        projects = current_app.db.research_projects.find()
        return [ResearchProject(p['title'], p['description'], str(p['_id']), p.get('finding_aid_ids', []), p.get('education_level')) for p in projects]

    @staticmethod
    def get_by_id(project_id):
        project = current_app.db.research_projects.find_one({'_id': ObjectId(project_id)})
        if project:
            return ResearchProject(project['title'], project['description'], str(project['_id']), project.get('finding_aid_ids', []), project.get('education_level'))
        return None

    @staticmethod
    def update(project_id, title, description, education_level):
        result = current_app.db.research_projects.update_one(
            {'_id': ObjectId(project_id)},
            {'$set': {'title': title, 'description': description, 'education_level': education_level}}
        )
        return result.modified_count > 0

    @staticmethod
    def delete(project_id):
        # Remove the project from all associated finding aids
        current_app.db.analyses.update_many(
            {"project_ids": project_id},
            {"$pull": {"project_ids": project_id}}
        )
        # Delete the project
        result = current_app.db.research_projects.delete_one({'_id': ObjectId(project_id)})
        return result.deleted_count > 0

    @staticmethod
    def add_finding_aid(project_id, finding_aid_id):
        result = current_app.db.research_projects.update_one(
            {'_id': ObjectId(project_id)},
            {'$addToSet': {'finding_aid_ids': finding_aid_id}}
        )
        return result.modified_count > 0

    @staticmethod
    def add_finding_aid(project_id, finding_aid_id):
        result = current_app.db.research_projects.update_one(
            {'_id': ObjectId(project_id)},
            {'$addToSet': {'finding_aid_ids': finding_aid_id}}
        )
        return result.modified_count > 0

    @staticmethod
    def get_finding_aids(project_id):
        project = current_app.db.research_projects.find_one({'_id': ObjectId(project_id)})
        if project and 'finding_aid_ids' in project:
            finding_aid_ids = [ObjectId(fid) for fid in project['finding_aid_ids']]
            finding_aids = current_app.db.finding_aids.find({'_id': {'$in': finding_aid_ids}})
            return list(finding_aids)
        return []

    @staticmethod
    def add_search_result(project_id, search_result):
        result = current_app.db.research_projects.update_one(
            {'_id': ObjectId(project_id)},
            {'$push': {'search_results': search_result}}
        )
        return result.modified_count > 0

    @staticmethod
    def get_search_results(project_id):
        project = current_app.db.research_projects.find_one({'_id': ObjectId(project_id)})
        if project and 'search_results' in project:
            return project['search_results']
        return []