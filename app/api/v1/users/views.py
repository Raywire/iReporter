"""Views for users"""
from flask_restful import Resource
from flask import jsonify, make_response
from app.api.v1.users.models import UserModel

db = UserModel()

def nonexistent_user():
    return jsonify({
        "status": 404,
        "error": "user does not exist"
    })

class Users(Resource):
    """Class with methods for getting and adding users"""


    def get(self):
        """method to get all users"""

        return make_response(jsonify({
            "status" : 200,
            "data" : db.get_users()
        }), 200)

    def post(self):
        """method to post a user"""
        user_id = db.save_user()

        if user_id == "keyerror":
            return make_response(jsonify({
                "status" : 400,
                "error" : "KeyError for email/password not posted"
            }), 400)

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


    def get(self, user_id):
        """method to get a specific user"""
        user = db.get_user(user_id)
        if user is None:
            return nonexistent_user()
        return make_response(jsonify({
            "status" : 200,
            "data" : user
        }), 200)

    def delete(self, user_id):
        """method to delete user"""
        user = db.get_user(user_id)
        
        if user is None:
            return nonexistent_user()

        delete_status = db.delete_user(user)
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
        user = db.get_user(user_id)

        if user is None:
            return nonexistent_user()

        edit_status = db.edit_user(user)
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


    def patch(self, user_id):
        """method to update user password"""
        user = db.get_user(user_id)       

        if user is None:
            return nonexistent_user()

        edit_status = db.edit_user_password(user)
        if edit_status == "keyerror":
            return make_response(jsonify({
                "status" : 400,
                "error" : "KeyError user's password not updated"
            }), 400)
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

    def patch(self, user_id):
        """method to update user status"""
        user = db.get_user(user_id)
        
        if user is None:
            return nonexistent_user()

        edit_status = db.edit_user_status(user)
        if edit_status == "keyerror":
            return make_response(jsonify({
                "status" : 400,
                "error" : "KeyError user's status not updated"
            }), 400)
        elif edit_status == "updated":
            success_message = {
                "id" : user_id,
                "message" : "Updated user's status"
            }
            return make_response(jsonify({
                "status" : 200,
                "data" : success_message
            }), 200)
