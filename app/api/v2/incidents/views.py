"""Views for red-flags"""
from flask_restful import Resource
from flask import jsonify, make_response
from app.api.v2.incidents.models import InterventionModel

class Interventions(Resource):
    """Class with methods for getting and adding redflags"""

    def __init__(self):
        self.db = InterventionModel()

    def post(self):
        """method to post a redflag"""
        intervention = self.db.save_intervention()
        return make_response(jsonify({
            "status" : 201,
            "data" : intervention
        }), 201)

