from src.config.blocklist import BLOCKLIST
from src.models.user_model import UserModel
from flask_restful import Resource, reqparse
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, jwt_required, get_jwt
import jwt


class Profile(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('refresh_token', type=str, required=False)

    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        user = UserModel.find_by_id(user_id)
        if not user:
            return {"error": True, "data": {"message": "User Not Found"}}, 404
        return {"error": False,
                "data": {
                    "message": "Profile obtained successfully.",
                    "user": user.json()
                }}, 200

    @jwt_required(fresh=True)
    def delete(self):
        data = self.parser.parse_args()
        if not data['refresh_token']:
            return {"error": True, "data": {"message": "No Refresh Token was Provided"}}, 400
        user_id = get_jwt_identity()
        user = UserModel.find_by_id(user_id)
        if not user:
            return {"error": True, "data": {"message": "User Not Found"}}, 404
        user.delete_from_db()
        decoded_refresh_token = jwt.decode(data['refresh_token'], options={"verify_signature": False})
        jti_access_token = get_jwt()['jti']
        jti_refresh_token = decoded_refresh_token['jti']
        BLOCKLIST.add(jti_access_token)
        BLOCKLIST.add(jti_refresh_token)
        return {"error": False, "data": {"message": "User deleted successfully"}}, 200


class UserLogout(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('refresh_token', type=str, required=False)

    @jwt_required()
    def post(self):
        data = self.parser.parse_args()
        if not data['refresh_token']:
            return {"error": True, "data": {"message": "No Refresh Token was Provided"}}, 400
        decoded_refresh_token = jwt.decode(data['refresh_token'], options={"verify_signature": False})
        jti_access_token = get_jwt()['jti']
        jti_refresh_token = decoded_refresh_token['jti']
        BLOCKLIST.add(jti_access_token)
        BLOCKLIST.add(jti_refresh_token)
        return {"error": False, "data": {"message": "Logged Out Successfully"}}, 200


class UserLogin(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('email', type=str, required=False)
    parser.add_argument('password', type=str, required=False)

    @classmethod
    def post(cls):
        data = cls.parser.parse_args()
        if not data['email'] or not data['password']:
            return {"error": True, "data": {"message": "Email or Password is missing"}}, 400
        user = UserModel.find_by_email(data['email'])
        if user and check_password_hash(user.password, data['password']):
            access_token = create_access_token(identity=user.user_id, fresh=True)
            refresh_token = create_refresh_token(identity=user.user_id)
            return {"error": False,
                    "data": {
                        "message": "Logged In Successfully",
                        "access_token": access_token,
                        "refresh_token": refresh_token,
                        "user": user.json()
                    }}, 200
        return {"error": True, "data": {"message": "Invalid Credentials"}}, 401


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=False)
    parser.add_argument('email', type=str, required=False)
    parser.add_argument('password', type=str, required=False)

    @classmethod
    def post(cls):
        data = cls.parser.parse_args()
        if not data['email'] or not data['username'] or not data['password']:
            return {"error": True, "data": {"message": "Email, Username or Password is missing"}}, 400
        if UserModel.find_by_email(data['email']) or UserModel.find_by_username(data['username']):
            return {"error": True, "data": {"message": "Email or Username is not valid. Try Again"}}, 400
        data['password'] = generate_password_hash(data['password'])
        user = UserModel(**data)
        access_token = create_access_token(identity=user.user_id, fresh=True)
        refresh_token = create_refresh_token(identity=user.user_id)
        user.save_to_db()
        return {"error": False,
                "data": {
                    "message": "User created successfully",
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                    "user": user.json()
                }}, 201


class TokenRefresh(Resource):

    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity()
        access_token = create_access_token(identity=current_user, fresh=False)
        refresh_token = create_refresh_token(identity=current_user)
        return {"error": False,
                "data": {
                    "message": "Refreshed Token Successfully",
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                }}, 200
