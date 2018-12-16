"""Views for users"""
from flask_restplus import Resource
from flask import jsonify, request
from app.api.v2.users.models import UserModel
from app.api.v2.decorator import token_required

import jwt
import datetime
import os

secret_key = os.getenv('SECRET_KEY')
expiration_time = 59


def nonexistent_user():
    return jsonify({
        "status": 200,
        "message": "user does not exist"
    })


def admin_user():
    return jsonify({
        "status": 200,
        "message": "Only admin can access this route"
    })


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

        token = jwt.encode({'public_id': user['public_id'], 'exp': datetime.datetime.utcnow(
        ) + datetime.timedelta(minutes=expiration_time)}, secret_key, algorithm='HS256')
        return jsonify({
            "status": 201,
            "data": [
                {
                    "token": token.decode('UTF-8'),
                    "user": user
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
            return nonexistent_user()
        if user is False:
            return jsonify({
                "status": 200,
                "message": "password is invalid"
            })

        token = jwt.encode({'public_id': user['public_id'], 'exp': datetime.datetime.utcnow(
        ) + datetime.timedelta(minutes=expiration_time)}, secret_key, algorithm='HS256')
        return jsonify({
            "status": 200,
            "data": [
                {
                    "token": token.decode('UTF-8'),
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
        user = self.db.get_user_by_username(username)
        if user is None:
            return nonexistent_user()
        return jsonify({
            "status": 200,
            "data": user
        })

    @token_required
    def delete(current_user, self, username):
        """method to delete user"""
        user = self.db.get_user_by_username(username)

        if user is None:
            return nonexistent_user()

        if current_user['isadmin'] is not True:
            return jsonify({
                "status": 401,
                "message": "Only an admin can delete a user"
            })

        delete_status = self.db.delete_user(username)
        if delete_status is True:
            success_message = {
                "username": username,
                "message": "user record has been deleted"
            }
            return jsonify({
                "status": 200,
                "data": success_message
            })


class UserStatus(Resource):
    """Class with method for updating a  specific user admin status"""

    def __init__(self):
        self.db = UserModel()

    @token_required
    def patch(current_user, self, username):
        """method to promote user"""
        user = self.db.get_user_by_username(username)

        if user is None:
            return nonexistent_user()

        if current_user['isadmin'] is not True:
            return jsonify({
                "status": 401,
                "message": "Only an admin can change the status of a user"
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
