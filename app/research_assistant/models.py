from bson import ObjectId
from flask import current_app

class ResearchProject:
    def __init__(self, title, description, _id=None):
        self.title = title
        self.description = description
        self._id = _id

    @staticmethod
    def create(title, description):
        project = {
            'title': title,
            'description': description
        }
        result = current_app.db.research_projects.insert_one(project)
        return str(result.inserted_id)

    @staticmethod
    def get_all():
        projects = current_app.db.research_projects.find()
        return [ResearchProject(p['title'], p['description'], str(p['_id'])) for p in projects]

    @staticmethod
    def get_by_id(project_id):
        project = current_app.db.research_projects.find_one({'_id': ObjectId(project_id)})
        if project:
            return ResearchProject(project['title'], project['description'], str(project['_id']))
        return None

    @staticmethod
    def update(project_id, title, description):
        result = current_app.db.research_projects.update_one(
            {'_id': ObjectId(project_id)},
            {'$set': {'title': title, 'description': description}}
        )
        return result.modified_count > 0

    @staticmethod
    def delete(project_id):
        result = current_app.db.research_projects.delete_one({'_id': ObjectId(project_id)})
        return result.deleted_count > 0

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