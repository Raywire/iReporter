"""Views for users"""
from flask_restful import Resource
from flask import jsonify, make_response
from app.api.v1.users.models import UserModel

class Users(Resource):
    """Class with methods for getting and adding users"""

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

        if user_id == "email exists":
            return make_response(jsonify({
                "status" : 400,
                "error" : "email already exists"
            }), 400)

        if user_id == "username exists":
            return make_response(jsonify({
                "status" : 400,
                "error" : "username already exists"
            }), 400)            

        success_message = {
            "id" : user_id,
            "message" : "Created user record"
        }

        return make_response(jsonify({
            "status" : 201,
            "data" : success_message
        }), 201)

class User(Resource):
    """Class with methods for getting, deleting and updating a  specific user"""

    def __init__(self):
        self.db = UserModel()

    def get(self, user_id):
        """method to get a specific user"""
        user = self.db.get_user(user_id)
        if user == "no user":
            return make_response(jsonify({
                "status" : 404,
                "error" : "user does not exist"
            }), 404)
        return make_response(jsonify({
            "status" : 200,
            "data" : user
        }), 200)

    def delete(self, user_id):
        """method to delete user"""
        user = self.db.get_user(user_id)
        
        if user == "no user":
            return make_response(jsonify({
                "status" : 404,
                "error" : "user does not exist"
            }), 404)
        delete_status = self.db.delete_user(user)
        if delete_status == "deleted":
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
        user = self.db.get_user(user_id)

        if user == "no user":
            return make_response(jsonify({
                "status" : 404,
                "error" : "user does not exist"
            }), 404)

        edit_status = self.db.edit_user(user)
        if edit_status == "updated":
            success_message = {
                "id" : user_id,
                "message" : "user record has been updated"
            }
            return make_response(jsonify({
                "status" : 200,
                "data" : success_message
            }))

class UpdateUserPassword(Resource):
    """Class with method for updating user's password"""

    def __init__(self):
        self.db = UserModel()

    def patch(self, user_id):
        """method to update user password"""
        user = self.db.get_user(user_id)       

        if user == "no user":
            return make_response(jsonify({
                "status" : 404,
                "error" : "User does not exist"
            }), 404)

        edit_status = self.db.edit_user_password(user)
        if edit_status == "keyerror":
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
    """class with method for updating user's status"""

    def __init__(self):
        self.db = UserModel()

    def patch(self, user_id):
        """method to update user status"""
        user = self.db.get_user(user_id)
        
        if user == "no user":
            return make_response(jsonify({
                "status" : 404,
                "error" : "User does not exist"
            }), 404)

        edit_status = self.db.edit_user_status(user)
        if edit_status == "keyerror":
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
