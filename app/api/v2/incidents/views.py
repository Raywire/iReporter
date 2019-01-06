"""Views for incidents"""
from flask_restful import Resource
from flask import jsonify
from app.api.v2.incidents.models import IncidentModel
from app.api.v2.send_email import send
from app.api.v2.decorator import (
    token_required, nonexistent_incident, owner_can_edit, draft_is_deletable, draft_is_editable, updated_incident)


class Interventions(Resource):
    """Contains methods for getting and adding interventions"""

    def __init__(self):
        self.intervention_model = IncidentModel()

    @token_required
    def post(current_user, self):
        """method to post one or multiple interventions"""
        intervention = self.intervention_model.save_incident(
            "intervention", current_user['id'])
        return jsonify({
            "status": 201,
            "data": [intervention]
        })

    @token_required
    def get(current_user, self):
        """method to get all interventions"""
        if self.intervention_model.get_incidents("intervention") is None:
            return jsonify({
                "status": 200,
                "data": [],
                "message" : "No interventions"
            })
        return jsonify({
            "status": 200,
            "data": self.intervention_model.get_incidents("intervention")
        })


class Intervention(Resource):
    """Contains methods for getting and deleting a  specific intervention"""

    def __init__(self):
        self.intervention_model = IncidentModel()

    @token_required
    def get(current_user, self, intervention_id):
        """method to get a specific intervention"""
        incident = self.intervention_model.get_incident_by_id(
            "intervention", intervention_id)
        if incident is None:
            return nonexistent_incident('Intervention')
        return jsonify({
            "status": 200,
            "data": [incident]
        })

    @token_required
    def delete(current_user, self, intervention_id):
        """method to delete intervention"""
        delete_status = self.intervention_model.delete_incident(
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
    """Contains method for updating an intervention's status"""

    def __init__(self):
        self.intervention_model = IncidentModel()

    @token_required
    def patch(current_user, self, intervention_id):
        """method to update intervention status"""
        if current_user['isadmin'] is False:
            return jsonify({
                "status": 401,
                "message": "Only an admin can change the status of the record"
            })
        edit_status = self.intervention_model.edit_incident_status(
            "intervention", intervention_id)

        if edit_status is None:
            return nonexistent_incident("Intervention")

        if edit_status is True:          
            status = self.intervention_model.get_incident_status()
            user_email = self.intervention_model.get_incident_by_id('intervention', intervention_id)['email']
            send(user_email, 'intervention',
                intervention_id, status)
            return updated_incident(intervention_id, "intervention", "status")


class UpdateInterventionLocation(Resource):
    """Contains method for updating an intervention's location"""

    def __init__(self):
        self.intervention_model = IncidentModel()

    @token_required
    def patch(current_user, self, intervention_id):
        """method to update intervention location"""
        intervention_type = "intervention"
        edit_status = self.intervention_model.edit_incident_location(
            intervention_type, intervention_id, current_user['id'])

        if edit_status is None:
            return nonexistent_incident("Intervention")

        if edit_status == 'not draft':
            return draft_is_editable()

        if edit_status is False:
            return owner_can_edit()

        if edit_status is True:
            return updated_incident(intervention_id, "intervention", "location")


class UpdateInterventionComment(Resource):
    """Contains method for updating an intervention's comment"""

    @token_required
    def patch(current_user, self, intervention_id):
        """method to update intervention comment"""
        edit_status = IncidentModel().edit_incident_comment(
            "intervention", intervention_id, current_user['id'])

        if edit_status is None:
            return jsonify({
                "status": 404,
                "message": "Intervention does not exist"
            })

        if edit_status is False:
            return owner_can_edit()

        if edit_status == 'not draft':
            return draft_is_editable()

        if edit_status:
            return jsonify({
                "status": 200,
                "data": [{
                    "id": intervention_id,
                    "message": "Updated intervention record's comment"
                }]
            })            


class Redflags(Resource):
    """Class with methods for getting and adding redflags"""

    @token_required
    def post(current_user, self):
        """method to post one or multiple redflags"""
        redflag = IncidentModel().save_incident(
            "redflag", current_user['id'])
        return jsonify({
            "status": 201,
            "data": [redflag]
        })

    @token_required
    def get(current_user, self):
        """method to get all redflags"""
        redflags = IncidentModel().get_incidents("redflag")
        if redflags is None:
            return jsonify({
                "status": 200,
                "data": [],
                "message" : "No interventions"
            })
        return jsonify({
            "status": 200,
            "data": redflags
        })


class Redflag(Resource):
    """Class with methods for getting and deleting specific redflag"""

    @token_required
    def get(current_user, self, redflag_id):
        """method to get a specific redflag"""
        incident = IncidentModel().get_incident_by_id("redflag", redflag_id)
        if incident is None:
            return nonexistent_incident("Redflag")
        return jsonify({
            "status": 200,
            "data": [incident]
        })

    @token_required
    def delete(current_user, self, redflag_id):
        """method to delete redflag"""
        delete_status = IncidentModel().delete_incident(
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

    @token_required
    def patch(current_user, self, redflag_id):
        """method to update redflag status"""
        if current_user['isadmin'] is False:
            return jsonify({
                "status": 401,
                "message": "Only an admin can change the status of a redflag"
            })
        edit_status = IncidentModel().edit_incident_status(
            "redflag", redflag_id)

        if edit_status is None:
            return nonexistent_incident("Redflag")

        if edit_status is True:
            email = IncidentModel().get_incident_by_id('redflag', redflag_id)['email']
            status = IncidentModel().get_incident_status()
            send(email, 'redflag', redflag_id, status)
            return updated_incident(redflag_id, "redflag", "status")


class UpdateRedflagLocation(Resource):
    """Class with method for updating an redflag's location"""

    @token_required
    def patch(current_user, self, redflag_id):
        """method to update redflag location"""
        edit_status = IncidentModel().edit_incident_location(
            "redflag", redflag_id, current_user['id'])

        if edit_status is None:
            return nonexistent_incident("Redflag")

        if edit_status == 'not draft':
            return draft_is_editable()

        if edit_status is False:
            return owner_can_edit()

        if edit_status is True:
            return updated_incident(redflag_id, "redflag", "location")


class UpdateRedflagComment(Resource):
    """Class with method for updating an redflag's comment"""
    def __init__(self):
        self.redflag_type = "redflag"

    @token_required
    def patch(current_user, self, redflag_id):
        """method to update redflag comment"""
        edit_status = IncidentModel().edit_incident_comment(
            self.redflag_type, redflag_id, current_user['id'])

        if edit_status is None:
            return nonexistent_incident("Redflag")

        if edit_status is False:
            return owner_can_edit()            

        if edit_status == 'not draft':
            return draft_is_editable()

        if edit_status is True:
            return updated_incident(redflag_id, self.redflag_type, "comment")
