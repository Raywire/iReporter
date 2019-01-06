"""Views for users"""
from flask_restful import Resource
from flask import jsonify, request
from app.api.v2.users.models import UserModel
from app.api.v2.decorator import token_required

import jwt
import datetime
import os

secret_key = os.getenv('SECRET_KEY')

try:
    expiration_time = int(os.getenv('EXPIRATION_TIME'))
except:
    expiration_time = 59


def nonexistent_user():
    return jsonify({
        "status": 404,
        "message": "user does not exist"
    })


def admin_user():
    return jsonify({
        "status": 403,
        "message": "Only admin can access this route"
    })

def get_token(public_id):
    token = jwt.encode({'public_id': public_id, 'exp': datetime.datetime.utcnow(
    ) + datetime.timedelta(minutes=expiration_time)}, secret_key, algorithm='HS256')
    return token    


class Users(Resource):
    """Class with methods for getting and adding users"""

    def __init__(self):
        self.db = UserModel()

    @token_required
    def get(current_user, self):
        """method to get all users"""
        if current_user['isadmin'] is False:
            return admin_user()
        return jsonify({
            "status": 200,
            "data": self.db.get_users()
        })


class UserSignUp(Resource):
    """Class with user signup post method"""

    def __init__(self):
        self.db = UserModel()

    def post(self):
        """method to post one or multiple users"""
        user = self.db.save_user()

        if user == "email exists":
            return jsonify({
                "status": 400,
                "message": "email already exists"
            })

        if user == "username exists":
            return jsonify({
                "status": 400,
                "message": "username already exists"
            })

        user_data = {
            "name" : user['firstname']+' '+user['lastname'],
            "usename" : user['username'],
            "email" : user['email'],
            "public_id" : user['public_id'],
            "isAdmin" : False
        }
        return jsonify({
            "status": 201,
            "message" : "You have been registered successfully",
            "data": [
                {
                    "token": get_token(user['public_id']).decode('UTF-8'),
                    "user": user_data
                }
            ]
        })


class UserSignIn(Resource):
    """Class containing user signin get method"""

    def __init__(self):
        self.db = UserModel()

    def post(self):
        """method to get a specific user"""
        user = self.db.sign_in()
                        
        if user is None:
            return jsonify({
                "status": 401,
                "message": "password or username is invalid"
            })
        if user is False:
            return jsonify({
                "status": 401,
                "message": "password or username is invalid"
            })

        return jsonify({
            "status": 200,
            "data": [
                {
                    "token": get_token(user['public_id']).decode('UTF-8'),
                    "user": user
                }
            ]
        })


class User(Resource):
    """Class with methods for getting and deleting a  specific user"""

    def __init__(self):
        self.db = UserModel()

    @token_required
    def get(current_user, self, username):
        """method to get a specific user"""
        if current_user['isadmin'] is False:
            return admin_user()
        user = self.db.get_user(username)
        if user is None:
            return nonexistent_user()
        user_data = {
            'id': user['id'], 'public_id': user['public_id'],
            'registered':user['registered'],'firstname': user['firstname'],
            'othernames': user['othernames'],'lastname': user['lastname'],
            'phoneNumber': user['phonenumber'],'email': user['email'],
            'username': user['username'],'isAdmin': user['isadmin']
            }            
        return jsonify({
            "status": 200,
            "data": [user_data]
        })

    @token_required
    def delete(current_user, self, username):
        """method to delete a user"""
        user = self.db.get_user(username)

        if user is None:
            return nonexistent_user()

        if current_user['isadmin'] is not True or user['id'] == 1 or current_user['username'] == username:
            return jsonify({
                "status": 403,
                "message": "You cannot delete this user"
            })

        delete_status = self.db.delete_user(username)
        if delete_status is True:

            return jsonify({
                "status": 200,
                "data": {
                    "username": username,
                    "message": "user record has been deleted"
                }
            })
        return jsonify({
            "status" : 400,
            "message": "A user who has posted incidents cannot be deleted"
        })

    @token_required
    def patch(current_user, self, username):
        """method to update a user's password"""

        if self.db.get_user(username) is None:
            return nonexistent_user()           

        if current_user['isadmin'] is True or current_user['username'] == username:
            if self.db.update_user_password(username) is True:
                return jsonify({
                    "status": 200,
                    "username": username,
                    "message": "User password has been changed"
                })

        return jsonify({
            "status": 403,
            "message": "Only an admin or the user can update their own password"
        })


class UserStatus(Resource):
    """Class with method for updating a  specific user admin status"""

    def __init__(self):
        self.db = UserModel()

    @token_required
    def patch(current_user, self, username):
        """method to promote a user"""
        user = self.db.get_user(username)

        if user is None:
            return nonexistent_user()

        if current_user['isadmin'] is not True or user['id'] == 1:
            return jsonify({
                "status": 403,
                "message": "You cannot change the status of this user"
            })

        if current_user['username'] == username:
            return jsonify({
              "status": 403,
              "message": "You cannot change your own admin status"  
            })            

        user_status_updated = self.db.promote_user(username)
        if user_status_updated is True:
            success_message = {
                "username": username,
                "message": "User status has been updated"
            }
            return jsonify({
                "status": 200,
                "data": success_message
            })
