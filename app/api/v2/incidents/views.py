"""Views for incidents"""
from flask_restful import Resource
from flask import jsonify, make_response
from app.api.v2.incidents.models import InterventionModel

class Interventions(Resource):
    """Class with methods for getting and adding interventions"""

    def __init__(self):
        self.db = InterventionModel()

    def post(self):
        """method to post one or multiple interventions"""
        intervention = self.db.save_intervention()
        return make_response(jsonify({
            "status" : 201,
            "data" : intervention
        }), 201)

    def get(self):
        """method to get all interventions"""

        return make_response(jsonify({
            "status" : 200,
            "data" : self.db.get_interventions()
        }), 200)

class Intervention(Resource):
    """Class with methods for getting, deleting and updating a  specific intervention"""

    def __init__(self):
        self.db = InterventionModel()

    def get(self, intervention_id):
        """method to get a specific intervention"""
        incident = self.db.get_intervention_by_id(intervention_id)
        if incident == None:
            return make_response(jsonify({
                "status" : 200,
                "error" : "Intervention does not exist"
            }), 200)
        return make_response(jsonify({
            "status" : 200,
            "data" : incident
        }), 200)

    def delete(self, intervention_id):
        """method to delete intervention"""
        delete_status = self.db.delete_intervention(intervention_id)

        if delete_status == None:
            return make_response(jsonify({
                "status" : 200,
                "error" : "Intervention does not exist"
            }), 200)

        if delete_status == "deleted":
            return make_response(jsonify({
                "status" : 200,
                "data" : {
                    "id" : intervention_id,
                    "message" : "Intervention record has been deleted"
                }
            }), 200)

class UpdateInterventionStatus(Resource):
    """Class with method for updating an intervention's status"""

    def __init__(self):
        self.db = InterventionModel()

    def patch(self, intervention_id):
        """method to update intervention status"""
        edit_status = self.db.edit_intervention_status(intervention_id)

        if edit_status == None:
            return make_response(jsonify({
                "status" : 200,
                "message" : "Intervention does not exist"
            }), 200)
        
        if edit_status == "updated":
            return make_response(jsonify({
                "status" : 200,
                "data" : {
                    "id" : intervention_id,
                    "message" : "Updated intervention record status"
                }
            }), 200)

class UpdateInterventionLocation(Resource):
    """Class with method for updating an intervention's location"""

    def __init__(self):
        self.db = InterventionModel()

    def patch(self, intervention_id):
        """method to update intervention location"""
        edit_status = self.db.edit_intervention_location(intervention_id)

        if edit_status == None:
            return make_response(jsonify({
                "status" : 200,
                "message" : "Intervention does not exist"
            }), 200)
        
        if edit_status == "updated":
            return make_response(jsonify({
                "status" : 200,
                "data" : {
                    "id" : intervention_id,
                    "message" : "Updated intervention record's location"
                }
            }), 200)

class UpdateInterventionComment(Resource):
    """Class with method for updating an intervention's comment"""

    def __init__(self):
        self.db = InterventionModel()

    def patch(self, intervention_id):
        """method to update intervention comment"""
        edit_status = self.db.edit_intervention_comment(intervention_id)

        if edit_status == None:
            return make_response(jsonify({
                "status" : 200,
                "message" : "Intervention does not exist"
            }), 200)
        
        if edit_status == "updated":
            return make_response(jsonify({
                "status" : 200,
                "data" : {
                    "id" : intervention_id,
                    "message" : "Updated intervention record's comment"
                }
            }), 200)