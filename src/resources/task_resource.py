from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.models.task_model import TaskModel


class TaskCreation(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('title', type=str, required=False)
    parser.add_argument('description', type=str, required=False)
    parser.add_argument('done', type=bool, required=False)

    @jwt_required()
    def post(self):
        user_id = get_jwt_identity()
        print(user_id)
        if not user_id:
            return {"error": True, "data": {"message": "User Id is Required"}}, 400
        data = self.parser.parse_args()
        if not data['title']:
            return {"error": True, "data": {"message": "Title is Required"}}, 400
        task = TaskModel(user_id, **data)
        task.save_to_db()
        return {"error": False,
                "data": {
                    "message": "Task created successfully",
                    "task": task.json()
                }}, 201


class TaskList(Resource):

    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        print(user_id)
        tasks = [task.json() for task in TaskModel.find_all_by_user_id(user_id)]
        return {"error": False,
                "data": {
                    "message": "User Tasks Found",
                    "tasks": tasks
                }}, 200
