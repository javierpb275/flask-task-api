from config.db import db
from os import environ
from dotenv import load_dotenv
from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager
from resources.user_resource import UserRegister, UserLogin, UserLogout, TokenRefresh, Profile
from datetime import timedelta

from src.config.blocklist import BLOCKLIST

app = Flask(__name__)

load_dotenv('config/.env')

app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('SQLALCHEMY_DATABASE_URI')
app.config['JWT_SECRET_KEY'] = environ.get('JWT_SECRET_KEY')
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)

db.init_app(app)

jwt = JWTManager(app)


@jwt.token_in_blocklist_loader
def check_if_token_in_blocklist(jwt_header, jwt_data):
    return jwt_data['jti'] in BLOCKLIST


@jwt.revoked_token_loader
def revoked_token_callback(jwt_header, jwt_data):
    return jsonify({'error': True, 'data': {
        'message': 'The token has been revoked.',
        'error': 'token_revoked'
    }}), 401


@jwt.expired_token_loader
def expired_token_callback():
    return jsonify({'error': True, 'data': {
        'message': 'The token has expired.',
        'error': 'token_expired'
    }}), 401


@jwt.invalid_token_loader
def invalid_token_callback(error):
    return jsonify({'error': True, 'data': {
        'message': 'Signature verification failed.',
        'error': 'invalid_token'
    }}), 401


@jwt.unauthorized_loader
def missing_token_callback(error):
    return jsonify({'error': True, 'data': {
        'message': 'Request does not contain an access token.',
        'error': 'authorization_required'
    }}), 401


@jwt.needs_fresh_token_loader
def token_not_fresh_callback(error):
    return jsonify({'error': True, 'data': {
        'message': 'The token is not fresh.',
        'error': 'fresh_token_required'
    }}), 401


api = Api(app)

api.add_resource(TokenRefresh, '/users/refresh')
api.add_resource(UserRegister, '/users/register')
api.add_resource(UserLogin, '/users/login')
api.add_resource(UserLogout, '/users/logout')
api.add_resource(Profile, '/users/me')
