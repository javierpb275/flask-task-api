from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.models.task_model import TaskModel


class Task(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('title', type=str, required=False)
    parser.add_argument('description', type=str, required=False)
    parser.add_argument('done', type=bool, required=False)

    @jwt_required()
    def get(self, task_id):
        user_id = get_jwt_identity()
        task = TaskModel.find_by_user_id_and_id(user_id, task_id)
        if not task:
            return {"error": True, "data": {"message": "Task Not Found"}}, 404
        return {"error": False,
                "data": {
                    "message": "Task Found successfully.",
                    "task": task.json()
                }}, 200

    @jwt_required(fresh=True)
    def delete(self, task_id):
        user_id = get_jwt_identity()
        task = TaskModel.find_by_user_id_and_id(user_id, task_id)
        if not task:
            return {"error": True, "data": {"message": "Task Not Found"}}, 404
        task.delete_from_db()
        return {"error": False, "data": {"message": "Task Deleted Successfully"}}, 200

    @jwt_required()
    def patch(self, task_id):
        user_id = get_jwt_identity()
        task = TaskModel.find_by_user_id_and_id(user_id, task_id)
        if not task:
            return {"error": True, "data": {"message": "Task Not Found"}}, 404
        data = self.parser.parse_args()
        if data['title']:
            task.title = data['title']
        if data['description']:
            task.description = data['description']
        if data['done']:
            task.done = data['done']
        task.save_to_db()
        return {"error": False,
                "data": {
                    "message": "Task Updated Successfully",
                    "user": task.json()
                }}, 200


class TaskCreation(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('title', type=str, required=False)
    parser.add_argument('description', type=str, required=False)
    parser.add_argument('done', type=bool, required=False)

    @jwt_required()
    def post(self):
        user_id = get_jwt_identity()
        if not user_id:
            return {"error": True, "data": {"message": "User Id is Required"}}, 400
        data = self.parser.parse_args()
        if not data['title']:
            return {"error": True, "data": {"message": "Title is Required"}}, 400
        task = TaskModel(user_id, **data)
        task.save_to_db()
        return {"error": False,
                "data": {
                    "message": "Task Created Successfully",
                    "task": task.json()
                }}, 201


class TaskList(Resource):

    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        tasks = [task.json() for task in TaskModel.find_all_by_user_id(user_id)]
        return {"error": False,
                "data": {
                    "message": "User Tasks Found",
                    "tasks": tasks
                }}, 200
