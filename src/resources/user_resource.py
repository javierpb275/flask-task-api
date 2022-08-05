from src.models.user_model import UserModel
from flask_restful import Resource, reqparse
from werkzeug.security import generate_password_hash

_user_parser = reqparse.RequestParser()
_user_parser.add_argument('username',
                          type=str,
                          required=True,
                          help="This field cannot be blank."
                          )
_user_parser.add_argument('email',
                          type=str,
                          required=True,
                          help="This field cannot be blank."
                          )
_user_parser.add_argument('password',
                          type=str,
                          required=True,
                          help="This field cannot be blank."
                          )


class UserRegister(Resource):

    @classmethod
    def post(cls):
        data = _user_parser.parse_args()
        if UserModel.find_by_email(data['email']) or UserModel.find_by_username(data['username']):
            return {"message": "Wrong Information. Try Again."}, 400
        data['password'] = generate_password_hash(data['password'])
        user = UserModel(**data)
        user.save_to_db()
        return {"message": "User created successfully."}, 201
