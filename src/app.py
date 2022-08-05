from config.db import db
from os import environ
from dotenv import load_dotenv
from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from resources.user_resource import UserRegister

app = Flask(__name__)

load_dotenv('config/.env')

app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['JWT_SECRET_KEY'] = environ.get('JWT_SECRET_KEY')

db.init_app(app)

jwt = JWTManager(app)

api = Api(app)

api.add_resource(UserRegister, '/users/register')

