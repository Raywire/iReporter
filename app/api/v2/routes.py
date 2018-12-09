"""v2 module init file"""
from flask_restful import Api
from flask import Blueprint
from app.api.v2.users.views import User, Users, UserSignUp, UserSignIn
from app.api.v2.incidents.views import Intervention, Interventions, UpdateInterventionStatus, UpdateInterventionLocation, UpdateInterventionComment
from app.api.v2.incidents.views import Redflag, Redflags, UpdateRedflagStatus, UpdateRedflagLocation, UpdateRedflagComment

VERSION_TWO = Blueprint('api_v2', __name__, url_prefix='/api/v2')

API = Api(VERSION_TWO)

API.add_resource(Users, '/users')
API.add_resource(UserSignUp, '/auth/signup')
API.add_resource(UserSignIn, '/auth/login')
API.add_resource(User, '/users/<username>')
API.add_resource(Interventions, '/interventions')
API.add_resource(Intervention, '/interventions/<int:intervention_id>')
API.add_resource(UpdateInterventionStatus, '/interventions/<int:intervention_id>/status')
API.add_resource(UpdateInterventionLocation, '/interventions/<int:intervention_id>/location')
API.add_resource(UpdateInterventionComment, '/interventions/<int:intervention_id>/comment')
API.add_resource(Redflag, '/redflags/<int:redflag_id>')
API.add_resource(Redflags, '/redflags')
API.add_resource(UpdateRedflagStatus, '/redflags/<int:redflag_id>/status')
API.add_resource(UpdateRedflagLocation, '/redflags/<int:redflag_id>/location')
API.add_resource(UpdateRedflagComment, '/redflags/<int:redflag_id>/comment')

