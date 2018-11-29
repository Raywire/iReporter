from redflags.views import RedFlags, RedFlag, UpdateRedFlagLocation

from flask import Blueprint
from flask_restful import Api, Resource

version_one = Blueprint('api_v1', __name__, url_prefix = '/api/v1')

api = Api(version_one)

api.add_resource(RedFlags, '/red-flags')
api.add_resource(RedFlag, '/red-flags/<int:redflag_id>')
api.add_resource(UpdateRedFlagLocation, '/red-flags/<int:redflag_id>/location')

