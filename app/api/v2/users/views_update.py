"""Views for users"""
from flask_restful import Resource
from flask import jsonify
from app.api.v2.users.models import UserModel
from app.api.v2.decorator import token_required


class UserStatus(Resource):
    """Class with method for updating a  specific user admin status"""

    def __init__(self):
        self.db = UserModel()

    @token_required
    def patch(current_user, self, username):
        """method to promote a user"""
        user = self.db.get_user(username)

        if user is None:
            return jsonify({
                "status": 404,
                "message": "user does not exist"
            })

        if current_user['isadmin'] is not True or self.db.get_user(username)['id'] is 1:
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


class UserActivity(Resource):
    """Class with method for disabling or enabling user activity"""

    def __init__(self):
        self.db = UserModel()

    @token_required
    def patch(current_user, self, username):
        """method to deactivate/activate a user"""
        user = self.db.get_user(username)

        if user is None:
            return jsonify({
                "status": 404,
                "message": "user does not exist"
            })

        if current_user['isadmin'] is not True or user['id'] == 1:
            return jsonify({
                "status": 403,
                "message": "You cannot change this user's active status"
            })

        if current_user['username'] == username:
            return jsonify({
                "status": 403,
                "message": "You cannot change your own active status"
            })

        user_activity_updated = self.db.activate_user(username)
        if user_activity_updated is True:
            return jsonify({
                "status": 200,
                "data": {
                    "username": username,
                    "message": "User active status has been updated"
                }
            })
