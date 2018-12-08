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

