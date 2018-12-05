"""Views for red-flags"""
from flask_restful import Resource
from flask import jsonify, make_response
from app.api.v1.redflags.models import RedFlagModel

class RedFlags(Resource):
    """Class with methods for getting and adding redflags"""

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
        redflag = self.db.save_redflag()
        if 'id' in redflag:
            return make_response(jsonify({
                "status" : 201,
                "data" : redflag
            }), 201)
        return make_response(jsonify({
            "status" : 400,
            "missing keys" : redflag
        }), 400)

class RedFlag(Resource):
    """Class with methods for getting, deleting and updating a  specific redflag"""

    def __init__(self):
        self.db = RedFlagModel()

    def get(self, redflag_id):
        """method to get a specific redflag"""
        incident = self.db.get_redflag(redflag_id)
        if incident == "no redflag":
            return make_response(jsonify({
                "status" : 200,
                "error" : "Red-flag does not exist"
            }), 200)
        return make_response(jsonify({
            "status" : 200,
            "data" : incident
        }), 200)

    def delete(self, redflag_id):
        """method to delete redflag"""
        incident = self.db.get_redflag(redflag_id)

        if incident == "no redflag":
            return make_response(jsonify({
                "status" : 200,
                "error" : "Red-flag does not exist"
            }), 200)
        delete_status = self.db.delete_redflag(incident)
        if delete_status == "deleted":
            return make_response(jsonify({
                "status" : 200,
                "data" : {
                    "id" : redflag_id,
                    "message" : "red-flag record has been deleted"
                }
            }), 200)

    def put(self, redflag_id):
        """method to update a redflag"""
        incident = self.db.get_redflag(redflag_id)       

        if incident == "no redflag":
            return make_response(jsonify({
                "status" : 200,
                "error" : "Red-flag does not exist"
            }), 200)
        edit_status = self.db.edit_redflag(incident)
        if edit_status == "updated":
            return make_response(jsonify({
                "status" : 200,
                "data" : {
                    "id" : redflag_id,
                    "message" : "red-flag record has been updated"
                }
            }))

class UpdateRedFlagLocation(Resource):
    """Class with method for updating a redflag's location"""

    def __init__(self):
        self.db = RedFlagModel()

    def patch(self, redflag_id):
        """method to update redflag location"""
        incident = self.db.get_redflag(redflag_id)

        if incident == "no redflag":
            return make_response(jsonify({
                "status" : 200,
                "error" : "Red-flag does not exist"
            }), 200)
        edit_status = self.db.edit_redflag_location(incident)
        if edit_status == "keyerror":
            return make_response(jsonify({
                "status" : 400,
                "error" : "KeyError Red-flag's location not updated"
            }), 400)
        elif edit_status == "updated":
            return make_response(jsonify({
                "status" : 200,
                "data" : {
                    "id" : redflag_id,
                    "message" : "Updated red-flag record's location"
                }
            }), 200)

class UpdateRedFlagComment(Resource):
    """Class with method for updating a redflag's comment"""

    def __init__(self):
        self.db = RedFlagModel()

    def patch(self, redflag_id):
        """method to update comment in a redflag"""
        incident = self.db.get_redflag(redflag_id)

        if incident == "no redflag":
            return make_response(jsonify({
                "status" : 200,
                "error" : "Red-flag does not exist"
            }), 200)

        edit_status = self.db.edit_redflag_comment(incident)
        if edit_status == "keyerror":
            return make_response(jsonify({
                "status" : 400,
                "error" : "KeyError Red-flag's comment not updated"
            }), 400)
        elif edit_status == "updated":
            return make_response(jsonify({
                "status" : 200,
                "data" : {
                    "id" : redflag_id,
                    "message" : "Updated red-flag record's comment"
                }
            }), 200)
