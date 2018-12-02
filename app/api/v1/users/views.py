"""Views for users"""
from flask_restful import Resource
from flask import jsonify, make_response
from app.api.v1.users.models import UserModel

class Users(Resource):
    """docstring for users"""

    def __init__(self):
        self.db = UserModel()

    def get(self):
        """method to get all users"""

        return make_response(jsonify({
            "status" : 200,
            "data" : self.db.get_users()
        }), 200)

    def post(self):
        """method to post a user"""
        user_id = self.db.save_user()

        if user_id == "keyerror":
            return make_response(jsonify({
                "status" : 500,
                "error" : "KeyError for email/password not posted"
            }), 500)
        success_message = {
            "id" : user_id,
            "message" : "Created user record"
        }

        return make_response(jsonify({
            "status" : 201,
            "data" : success_message
        }), 201)

class User(Resource):
    """docstring of User"""

    def __init__(self):
        self.db = UserModel()

    def get(self, user_id):
        """method to get a specific user"""
        incident = self.db.get_user(user_id)
        if incident == "no user":
            return make_response(jsonify({
                "status" : 404,
                "error" : "user does not exist"
            }), 404)
        return make_response(jsonify({
            "status" : 200,
            "data" : incident
        }), 200)

    def delete(self, user_id):
        """method to delete user"""
        delete_status = self.db.delete_user(user_id)
        if delete_status == "no user":
            return make_response(jsonify({
                "status" : 404,
                "error" : "user does not exist"
            }), 404)
        elif delete_status == "deleted":
            success_message = {
                "id" : user_id,
                "message" : "user record has been deleted"
            }
            return make_response(jsonify({
                "status" : 200,
                "data" : success_message
            }))

    def put(self, user_id):
        """method to update a user"""
        edit_status = self.db.edit_user(user_id)

        if edit_status == "no user":
            return make_response(jsonify({
                "status" : 404,
                "error" : "user does not exist"
            }), 404)
        elif edit_status == "updated":
            success_message = {
                "id" : user_id,
                "message" : "user record has been updated"
            }
            return make_response(jsonify({
                "status" : 200,
                "data" : success_message
            }))

class UpdateUserPassword(Resource):
    """docstring of UpdateUserPassword"""

    def __init__(self):
        self.db = UserModel()

    def patch(self, user_id):
        """method to update user password"""

        edit_status = self.db.edit_user_password(user_id)

        if edit_status == "no user":
            return make_response(jsonify({
                "status" : 404,
                "error" : "User does not exist"
            }), 404)

        elif edit_status == "keyerror":
            return make_response(jsonify({
                "status" : 500,
                "error" : "KeyError user's password not updated"
            }), 500)
        elif edit_status == "updated":
            success_message = {
                "id" : user_id,
                "message" : "Updated user's password"
            }
            return make_response(jsonify({
                "status" : 200,
                "data" : success_message
            }), 200)

class UpdateUserStatus(Resource):
    """docstring of UpdateUserStatus"""

    def __init__(self):
        self.db = UserModel()

    def patch(self, user_id):
        """method to update user status"""

        edit_status = self.db.edit_user_status(user_id)

        if edit_status == "no user":
            return make_response(jsonify({
                "status" : 404,
                "error" : "User does not exist"
            }), 404)

        elif edit_status == "keyerror":
            return make_response(jsonify({
                "status" : 500,
                "error" : "KeyError user's status not updated"
            }), 500)
        elif edit_status == "updated":
            success_message = {
                "id" : user_id,
                "message" : "Updated user's status"
            }
            return make_response(jsonify({
                "status" : 200,
                "data" : success_message
            }), 200)
