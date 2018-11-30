"""Views for red-flags"""
from flask_restful import Resource
from flask import jsonify, make_response
from app.api.v1.redflags.models import RedFlagModel

class RedFlags(Resource):
    """docstring for RedFlags"""

    def __init__(self):
        self.db = RedFlagModel()

    def get(self):
        """method to get all redflags"""

        return make_response(jsonify({
            "status" : 200,
            "data" : self.db.get_redflags()
        }), 200)

    def post(self):
        """method to post a redflag"""
        redflag_id = self.db.save_redflag()

        if redflag_id == "keyerror":
            return make_response(jsonify({
                "status" : 500,
                "error" : "KeyError for createdBy Red-flag not posted"
            }), 500)
        success_message = {
            "id" : redflag_id,
            "message" : "Created red-flag record"
        }

        return make_response(jsonify({
            "status" : 201,
            "data" : success_message
        }), 201)

class RedFlag(Resource):
    """docstring of RedFlag"""

    def __init__(self):
        self.db = RedFlagModel()

    def get(self, redflag_id):
        """method to get a specific redflag"""
        incident = self.db.get_redflag(redflag_id)
        if incident == "no redflag":
            return make_response(jsonify({
                "status" : 404,
                "error" : "Red-flag does not exist"
            }), 404)
        return make_response(jsonify({
            "status" : 200,
            "data" : incident
        }), 200)

    def delete(self, redflag_id):
        """method to delete redflag"""
        delete_status = self.db.delete_redflag(redflag_id)
        if delete_status == "no redflag":
            return make_response(jsonify({
                "status" : 404,
                "error" : "Red-flag does not exist"
            }), 404)
        elif delete_status == "deleted":
            success_message = {
                "id" : redflag_id,
                "message" : "red-flag record has been deleted"
            }
            return make_response(jsonify({
                "status" : 200,
                "data" : success_message
            }))

    def put(self, redflag_id):
        """method to update a redflag"""
        edit_status = self.db.edit_redflag(redflag_id)

        if edit_status == "no redflag":
            return make_response(jsonify({
                "status" : 404,
                "error" : "Red-flag does not exist"
            }), 404)
        elif edit_status == "updated":
            success_message = {
                "id" : redflag_id,
                "message" : "red-flag record has been updated"
            }
            return make_response(jsonify({
                "status" : 200,
                "data" : success_message
            }))

class UpdateRedFlagLocation(Resource):
    """docstring of UpdateRedFlagLocation"""

    def __init__(self):
        self.db = RedFlagModel()

    def patch(self, redflag_id):
        """method to update redflag location"""

        edit_status = self.db.edit_redflag_location(redflag_id)

        if edit_status == "no redflag":
            return make_response(jsonify({
                "status" : 404,
                "error" : "Red-flag does not exist"
            }), 404)

        elif edit_status == "keyerror":
            return make_response(jsonify({
                "status" : 500,
                "error" : "KeyError Red-flag's location not updated"
            }), 500)
        elif edit_status == "updated":
            success_message = {
                "id" : redflag_id,
                "message" : "Updated red-flag record's location"
            }
            return make_response(jsonify({
                "status" : 200,
                "data" : success_message
            }), 200)

class UpdateRedFlagComment(Resource):
    """docstring of UpdateRedFlagComment"""

    def __init__(self):
        self.db = RedFlagModel()

    def patch(self, redflag_id):
        """method to update comment in a redflag"""
        edit_status = self.db.edit_redflag_comment(redflag_id)

        if edit_status == "no redflag":
            return make_response(jsonify({
                "status" : 404,
                "error" : "Red-flag does not exist"
            }), 404)

        elif edit_status == "keyerror":
            return make_response(jsonify({
                "status" : 500,
                "error" : "KeyError Red-flag's comment not updated"
            }), 500)
        elif edit_status == "updated":
            success_message = {
                "id" : redflag_id,
                "message" : "Updated red-flag record's comment"
            }
            return make_response(jsonify({
                "status" : 200,
                "data" : success_message
            }), 200)
