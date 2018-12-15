"""Views for incidents"""
from flask_restplus import Resource
from flask import jsonify, request
from app.api.v2.incidents.models import IncidentModel
from app.api.v2.users.models import UserModel
from functools import wraps
from app.api.v2.send_email import send

import jwt
import datetime
import os

secret_key = os.getenv('SECRET_KEY')

def token_required(f):
    @wraps(f)
    def decorated(*args, ** kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return {
                "message": "Token is missing"
            }, 401
        try:
            data = jwt.decode(token, secret_key, algorithms=['HS256'])
            current_user = UserModel().get_user_by_public_id(data['public_id'])
        except:
            return {
                "message": "Token is invalid"
            }, 401
        return f(current_user, *args, **kwargs)
    return decorated

class Interventions(Resource):
    """Class with methods for getting and adding interventions"""

    def __init__(self):
        self.db = IncidentModel()

    @token_required
    def post(current_user, self):
        """method to post one or multiple interventions"""
        intervention = self.db.save_incident(
            "intervention", current_user['id'])
        return jsonify({
            "status": 201,
            "data": [intervention]
        })

    @token_required
    def get(current_user, self):
        """method to get all interventions"""
        if self.db.get_incidents("intervention") is None:
            return jsonify({
                "status": 200,
                "message": "No interventions",
                "data": self.db.get_incidents("intervention")
            })
        return jsonify({
            "status": 200,
            "data": self.db.get_incidents("intervention")
        })

class Intervention(Resource):
    """Class with methods for getting, deleting and updating a  specific intervention"""

    def __init__(self):
        self.db = IncidentModel()

    @token_required
    def get(current_user, self, intervention_id):
        """method to get a specific intervention"""
        incident_type = "intervention"
        incident = self.db.get_incident_by_id(incident_type, intervention_id)
        if incident is None:
            return jsonify({
                "status": 200,
                "message": "Intervention does not exist"
            })
        return jsonify({
            "status": 200,
            "data": [incident]
        })

    @token_required
    def delete(current_user, self, intervention_id):
        """method to delete intervention"""
        delete_status = self.db.delete_incident(
            "intervention", intervention_id, current_user['id'])

        if delete_status is None:
            return jsonify({
                "status": 200,
                "message": "Intervention does not exist"
            })

        if delete_status == "no access":
            return jsonify({
                "status": 401,
                "message": "Only the user who created this intervention record can delete it"
            })

        if delete_status == "deleted":
            return jsonify({
                "status": 200,
                "data": {
                    "id": intervention_id,
                    "message": "Intervention record has been deleted"
                }
            })

class UpdateInterventionStatus(Resource):
    """Class with method for updating an intervention's status"""

    def __init__(self):
        self.db = IncidentModel()

    @token_required
    def patch(current_user, self, intervention_id):
        """method to update intervention status"""
        if current_user['isadmin'] is False:
            return jsonify({
                "status": 401,
                "message": "Only an admin can change the status of an intervention"
            })
        edit_status = self.db.edit_incident_status(
            "intervention", intervention_id)

        if edit_status is None:
            return jsonify({
                "status": 200,
                "message": "Intervention does not exist"
            })

        if edit_status == "updated":
            if current_user['email']:
                status = self.db.get_incident_status()
                send(current_user['email'], 'intervention', intervention_id, status)
            return jsonify({
                "status": 200,
                "data": [{
                    "id": intervention_id,
                    "message": "Updated intervention record status"
                }]
            })            

class UpdateInterventionLocation(Resource):
    """Class with method for updating an intervention's location"""

    def __init__(self):
        self.db = IncidentModel()

    @token_required
    def patch(current_user, self, intervention_id):
        """method to update intervention location"""
        edit_status = self.db.edit_incident_location(
            "intervention", intervention_id, current_user['id'])

        if edit_status is None:
            return jsonify({
                "status": 200,
                "message": "Intervention does not exist"
            })

        if edit_status == "no access":
            return jsonify({
                "status": 401,
                "message": "Only the user who created this intervention record can edit it"
            })

        if edit_status == "updated":
            return jsonify({
                "status": 200,
                "data": [{
                    "id": intervention_id,
                    "message": "Updated intervention record's location"
                }]
            })

class UpdateInterventionComment(Resource):
    """Class with method for updating an intervention's comment"""

    def __init__(self):
        self.db = IncidentModel()

    @token_required
    def patch(current_user, self, intervention_id):
        """method to update intervention comment"""
        edit_status = self.db.edit_incident_comment(
            "intervention", intervention_id, current_user['id'])

        if edit_status is None:
            return jsonify({
                "status": 200,
                "message": "Intervention does not exist"
            })

        if edit_status == "no access":
            return jsonify({
                "status": 401,
                "message": "Only the user who created this intervention record can edit it"
            })

        if edit_status == "updated":
            return jsonify({
                "status": 200,
                "data": [{
                    "id": intervention_id,
                    "message": "Updated intervention record's comment"
                }]
            })

class Redflags(Resource):
    """Class with methods for getting and adding redflags"""

    def __init__(self):
        self.db = IncidentModel()

    @token_required
    def post(current_user, self):
        """method to post one or multiple redflags"""
        intervention = self.db.save_incident("redflag", current_user['id'])
        return jsonify({
            "status": 201,
            "data": [intervention]
        })

    @token_required
    def get(current_user, self):
        """method to get all redflags"""
        redflags = self.db.get_incidents("redflag")
        if redflags is None:
            return jsonify({
                "status": 200,
                "message": "No redflags",
                "data": redflags
            })
        return jsonify({
            "status": 200,
            "data": redflags
        })


class Redflag(Resource):
    """Class with methods for getting, deleting and updating a  specific redflag"""

    def __init__(self):
        self.db = IncidentModel()

    @token_required
    def get(current_user, self, redflag_id):
        """method to get a specific redflag"""
        incident_type = "redflag"
        incident = self.db.get_incident_by_id(incident_type, redflag_id)
        if incident is None:
            return jsonify({
                "status": 200,
                "message": "Redflag does not exist"
            })
        return jsonify({
            "status": 200,
            "data": [incident]
        })

    @token_required
    def delete(current_user, self, redflag_id):
        """method to delete redflag"""
        delete_status = self.db.delete_incident(
            "redflag", redflag_id, current_user['id'])

        if delete_status is None:
            return jsonify({
                "status": 200,
                "message": "Redflag does not exist"
            })

        if delete_status == "no access":
            return jsonify({
                "status": 401,
                "message": "Only the user who created this redflag record can delete it"
            })

        if delete_status == "deleted":
            return jsonify({
                "status": 200,
                "data": {
                    "id": redflag_id,
                    "message": "Redflag record has been deleted"
                }
            })

class UpdateRedflagStatus(Resource):
    """Class with method for updating an redflag's status"""

    def __init__(self):
        self.db = IncidentModel()

    @token_required
    def patch(current_user, self, redflag_id):
        """method to update redflag status"""
        if current_user['isadmin'] is False:
            return jsonify({
                "status": 401,
                "message": "Only an admin can change the status of a redflag"
            })
        edit_status = self.db.edit_incident_status("redflag", redflag_id)

        if edit_status is None:
            return jsonify({
                "status": 200,
                "message": "Redflag does not exist"
            })

        if edit_status == "updated":
            if current_user['email']:
                status = self.db.get_incident_status()
                send(current_user['email'], 'redflag', redflag_id, status)            
            return jsonify({
                "status": 200,
                "data": [{
                    "id": redflag_id,
                    "message": "Updated redflag record status"
                }]
            })

class UpdateRedflagLocation(Resource):
    """Class with method for updating an redflag's location"""

    def __init__(self):
        self.db = IncidentModel()

    @token_required
    def patch(current_user, self, redflag_id):
        """method to update redflag location"""
        edit_status = self.db.edit_incident_location(
            "redflag", redflag_id, current_user['id'])

        if edit_status is None:
            return jsonify({
                "status": 200,
                "message": "Redflag does not exist"
            })

        if edit_status == "no access":
            return jsonify({
                "status": 401,
                "message": "Only the user who created this redflag record can edit it"
            })

        if edit_status == "updated":
            return jsonify({
                "status": 200,
                "data": [{
                    "id": redflag_id,
                    "message": "Updated redflag record's location"
                }]
            })


class UpdateRedflagComment(Resource):
    """Class with method for updating an redflag's comment"""

    def __init__(self):
        self.db = IncidentModel()

    @token_required
    def patch(current_user, self, redflag_id):
        """method to update redflag comment"""
        edit_status = self.db.edit_incident_comment(
            "redflag", redflag_id, current_user['id'])

        if edit_status is None:
            return jsonify({
                "status": 200,
                "message": "Redflag does not exist"
            })

        if edit_status == "no access":
            return jsonify({
                "status": 401,
                "message": "Only the user who created this redflag record can edit it"
            })

        if edit_status == "updated":
            return jsonify({
                "status": 200,
                "data": [{
                    "id": redflag_id,
                    "message": "Updated redflag record's comment"
                }]
            })
