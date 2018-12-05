"""v1 module init file"""
from flask_restful import Api
from flask import Blueprint
from app.api.v1.redflags.views import RedFlags, RedFlag, UpdateRedFlagComment, UpdateRedFlagLocation
from app.api.v1.users.views import User, Users, UpdateUserPassword, UpdateUserStatus

VERSION_ONE = Blueprint('api_v1', __name__, url_prefix='/api/v1')
errors = {
        'message': "Page not found",
        'status': 404
}

API = Api(VERSION_ONE, catch_all_404s=True, errors=errors)

API.add_resource(RedFlags, '/red-flags')
API.add_resource(RedFlag, '/red-flags/<int:redflag_id>')
API.add_resource(UpdateRedFlagLocation, '/red-flags/<int:redflag_id>/location')
API.add_resource(UpdateRedFlagComment, '/red-flags/<int:redflag_id>/comment')

API.add_resource(Users, '/users')
API.add_resource(User, '/users/<int:user_id>')
API.add_resource(UpdateUserPassword, '/users/<int:user_id>/password')
API.add_resource(UpdateUserStatus, '/users/<int:user_id>/status')
