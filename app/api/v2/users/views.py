"""Views for users"""
from flask_restful import Resource
from flask import jsonify, make_response
from app.api.v2.users.models import UserModel

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

class UserSignUp(Resource):
    """Class with user signup post method"""
    def __init__(self):
        self.db = UserModel()    
    def post(self):
        """method to post one or multiple users"""
        user = self.db.save_user()

        if user == "email exists":
            return make_response(jsonify({
                "status" : 400,
                "error" : "email already exists"
            }), 400)

        if user == "username exists":
            return make_response(jsonify({
                "status" : 400,
                "error" : "username already exists"
            }), 400)            

        return make_response(jsonify({
            "status" : 201,
            "data" : [
                {
                    "token" : "",
                    "user" : user
                }
            ]
        }), 201)

class User(Resource):
    """Class with methods for getting, deleting and updating a  specific user"""

    def __init__(self):
        self.db = UserModel()

    def get(self, username):
        """method to get a specific user"""
        user = self.db.get_user_by_username(username)
        if user == None:
            return make_response(jsonify({
                "status" : 200,
                "message" : "user does not exist"
            }), 200)
        return make_response(jsonify({
            "status" : 200,
            "data" : user
        }), 200)

    def delete(self, user_id):
        """method to delete user"""
        user = self.db.get_user(user_id)
        
        if user == "no user":
            return make_response(jsonify({
                "status" : 200,
                "error" : "user does not exist"
            }), 200)
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
