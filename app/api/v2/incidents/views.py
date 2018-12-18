"""Views for incidents"""
from flask_restful import Resource
from flask import jsonify
from app.api.v2.incidents.models import IncidentModel
from app.api.v2.send_email import send
from app.api.v2.decorator import token_required


def nonexistent_incident(incident_type):
    return jsonify({
        "status": 404,
        "message": "{0} does not exist".format(incident_type)
    })


def owner_can_edit():
    return jsonify({
        "status": 401,
        "message": "Only the user who created this record can edit it"
    })

def draft_is_editable():
    return jsonify({
        "status": 401,
        "message": "Incident can only be edited when the status is draft"
    })

def draft_is_deletable():
    return jsonify({
        "status": 401,
        "message": "Incident can only be deleted when the status is draft"
    })    

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
                "data": []
            })
        return jsonify({
            "status": 200,
            "data": self.db.get_incidents("intervention")
        })


class Intervention(Resource):
    """Class with methods for getting and deleting a  specific intervention"""

    def __init__(self):
        self.db = IncidentModel()

    @token_required
    def get(current_user, self, intervention_id):
        """method to get a specific intervention"""
        incident_type = "intervention"
        incident = self.db.get_incident_by_id(incident_type, intervention_id)
        if incident is None:
            return nonexistent_incident('Intervention')
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
            return nonexistent_incident("Intervention")

        if delete_status == 'not draft':
            return draft_is_deletable()

        if delete_status is False:
            return jsonify({
                "status": 401,
                "message": "Only the creator of this record can delete it"
            })

        if delete_status is True:
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
                "message": "Only an admin can change the status of the record"
            })
        edit_status = self.db.edit_incident_status(
            "intervention", intervention_id)

        if edit_status is None:
            return nonexistent_incident("Intervention")

        if edit_status is True:
            if current_user['email']:
                status = self.db.get_incident_status()
                send(current_user['email'], 'intervention',
                     intervention_id, status)
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
            return nonexistent_incident("Intervention")

        if edit_status == 'not draft':
            return draft_is_editable()            

        if edit_status is False:
            return owner_can_edit()

        if edit_status is True:
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
            return nonexistent_incident("Intervention")

        if edit_status == 'not draft':
            return draft_is_editable()           

        if edit_status is False:
            return owner_can_edit()

        if edit_status is True:
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
                "data": []
            })
        return jsonify({
            "status": 200,
            "data": redflags
        })


class Redflag(Resource):
    """Class with methods for getting and deleting specific redflag"""

    def __init__(self):
        self.db = IncidentModel()

    @token_required
    def get(current_user, self, redflag_id):
        """method to get a specific redflag"""
        incident_type = "redflag"
        incident = self.db.get_incident_by_id(incident_type, redflag_id)
        if incident is None:
            return nonexistent_incident("Redflag")
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
            return nonexistent_incident("Redflag")

        if delete_status == 'not draft':
            return draft_is_deletable()            

        if delete_status is False:
            return jsonify({
                "status": 401,
                "message": "Only the creator of this record can delete it"
            })

        if delete_status is True:
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
            return nonexistent_incident("Redflag")

        if edit_status is True:
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
            return nonexistent_incident("Redflag")

        if edit_status == 'not draft':
            return draft_is_editable()             

        if edit_status is False:
            return owner_can_edit()

        if edit_status is True:
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
            return nonexistent_incident("Redflag")

        if edit_status == 'not draft':
            return draft_is_editable()             

        if edit_status is False:
            return owner_can_edit()

        if edit_status is True:
            return jsonify({
                "status": 200,
                "data": [{
                    "id": redflag_id,
                    "message": "Updated redflag record's comment"
                }]
            })
