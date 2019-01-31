"""Views for users"""
from flask_restful import Resource
from flask import jsonify, request, current_app
from app.api.v2.users.models import UserModel
from app.api.v2.send_email import send
from app.api.v2.decorator import token_required

import jwt
import datetime
import os

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


def get_token(public_id, expiration):
    token = jwt.encode({'public_id': public_id, 'exp': datetime.datetime.utcnow(
    ) + datetime.timedelta(minutes=expiration)}, current_app.config['SECRET_KEY'], algorithm='HS256')
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
            "name": user['firstname']+' '+user['lastname'],
            "username": user['username'],
            "email": user['email'],
            "public_id": user['public_id'],
            "isAdmin": False
        }
        return jsonify({
            "status": 201,
            "message": "You have been registered successfully",
            "data": [
                {
                    "token": get_token(user['public_id'], expiration_time).decode('UTF-8'),
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

        if user is 'disabled':
            return jsonify({
                "status": 403,
                "message": "account has been disabled"
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
                    "token": get_token(user['public_id'], expiration_time).decode('UTF-8'),
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
        data = {
            'public_id': user['public_id'], 'isActive': user['isactive'],
            'registered': user['registered'], 'firstname': user['firstname'],
            'othernames': user['othernames'], 'lastname': user['lastname'],
            'phoneNumber': user['phonenumber'], 'email': user['email'],
            'username': user['username'], 'isAdmin': user['isadmin'],
            'photourl': self.db.get_profile_picture_url(user['photourl']),
            'emailVerified': user['emailverified']
        }
        return jsonify({
            "status": 200,
            "data": [data]
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
            "status": 400,
            "message": "A user who has posted incidents cannot be deleted"
        })

    @token_required
    def patch(current_user, self, username):
        """method to update a user's password"""

        if self.db.get_user(username) is None:
            return nonexistent_user()

        if current_user['isadmin'] is True or current_user['username'] == username:
            if self.db.update_user_password(username) is True:
                mail = self.db.get_user(username)['email']
                subject = "Password Updated"
                body = "Password for the account with username: {0} has been updated by {1}".format(
                    username, current_user['username'])
                send(mail, subject, body)
                return jsonify({
                    "status": 200,
                    "username": username,
                    "message": "User password has been changed"
                })

        return jsonify({
            "status": 403,
            "message": "Only an admin or the user can update their own password"
        })

    @token_required
    def put(current_user, self, username):
        """method to update a user's profile data"""

        user = self.db.update_user(username)

        if user is None:
            return nonexistent_user()

        if current_user['username'] != username:
            return jsonify({
                "status": 403,
                "message": "A user can only update their own profile"
            })

        if user == "email exists":
            return jsonify({
                "status": 400,
                "message": "email already exists"
            })

        return jsonify({
            "status": 200,
            "message": "Your profile has been updated",
            "data": [user]
        })


class UserResetPassword(Resource):
    """Class with method for sending reset password link to a user"""

    def post(self, email):
        """Method to request a password reset for a user email that exists"""
        user = UserModel().get_user(email)
        if user is None:
            return nonexistent_user()

        public_id = user['public_id']
        username = user['username']
        useremail = user['email']
        reset_token = get_token(public_id, 30).decode('UTF-8')
        json_reset_link = request.json.get('resetlink', None)

        if json_reset_link is None:
            return {
                "status": 400,
                "message": {
                    "resetlink": "This key is required"
                }
            }, 400

        reset_link = json_reset_link + '?username=' + username + '&token=' + reset_token
        reset_message = "If you did not make this request then simply ignore this email and no change will be made."
        subject = "Password Reset Request"
        body = "To reset your password visit the following link within half an hour: {0}\n{1}".format(
            reset_link, reset_message)
        if send(useremail, subject, body) is True:
            return jsonify({
                "status": 200,
                "message": "Reset link has been sent to your email"
            })
        return {
            "status": 400,
            "message": "Password reset failed please try again"
        }, 400


class RefreshUserToken(Resource):
    """Class with method to refresh a token"""
    @token_required
    def post(current_user, self, username):
        """method to get a specific user"""
        user = UserModel().get_user(username)
        if user is None:
            return nonexistent_user()
        if current_user['username'] != username:
            return {
                "status": 403,
                "message": "You can only refresh your own token"
            }, 403

        return jsonify({
            "status": 200,
            "message": "Token for {0} has been refreshed".format(username),
            "token": get_token(user['public_id'], expiration_time).decode('UTF-8')
        })
