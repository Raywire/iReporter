"""Views for users"""
from flask_restplus import Resource
from flask import jsonify, request
from app.api.v2.users.models import UserModel

import jwt
import datetime
import os

secret_key = os.getenv('SECRET_KEY')
expiration_time = 59


class Users(Resource):
    """Class with methods for getting and adding users"""

    def __init__(self):
        self.db = UserModel()

    def get(self):
        """method to get all users"""

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
        if user == None:
            return jsonify({
                "status": 200,
                "message": "user does not exist"
            })
        if user == 'invalid password':
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
    """Class with methods for getting, deleting and updating a  specific user"""

    def __init__(self):
        self.db = UserModel()

    def get(self, username):
        """method to get a specific user"""
        user = self.db.get_user_by_username(username)
        if user == None:
            return jsonify({
                "status": 200,
                "message": "user does not exist"
            })
        return jsonify({
            "status": 200,
            "data": user
        })

    def delete(self, user_id):
        """method to delete user"""
        user = self.db.get_user(user_id)

        if user == "no user":
            return jsonify({
                "status": 200,
                "error": "user does not exist"
            })
        delete_status = self.db.delete_user(user)
        if delete_status == "deleted":
            success_message = {
                "id": user_id,
                "message": "user record has been deleted"
            }
            return jsonify({
                "status": 200,
                "data": success_message
            })

    def patch(self, username):
        """method to promote user"""
        user = self.db.get_user_by_username(username)

        if user == None:
            return jsonify({
                "status": 200,
                "error": "user does not exist"
            })

        user_status = self.db.promote_user(username)
        if user_status == "updated":
            success_message = {
                "id": user_id,
                "message": "User status has been updated"
            }
            return jsonify({
                "status": 200,
                "data": success_message
            })
