"""v2 module init file"""
from flask_restful import Api
from flask import Blueprint
from app.api.v2.users.views import User, Users, UserSignUp

VERSION_TWO = Blueprint('api_v2', __name__, url_prefix='/api/v2')

API = Api(VERSION_TWO)

API.add_resource(Users, '/users')
API.add_resource(UserSignUp, '/auth/signup')
API.add_resource(User, '/users/<username>')