"""User Models"""
import datetime
from flask import request

USERS = []

class UserModel:
    """user model class"""
    def __init__(self):
        self.db = USERS
        if not self.db:
            self.id = 1
        else:
            self.id = self.db[-1]['id'] + 1

    def get_users(self):
        """method to get all users"""
        return self.db

    def save_user(self):
        """method to post a user"""
        data = {
            'id' : self.id,
            'firstname' : request.json.get('firstname', ''),
            'lastname' : request.json.get('lastname', ''),
            'othernames' : request.json.get('othernames', ''),
            'email' : request.json.get('email', 'keyerror'),
            'phoneNumber' : request.json.get('phoneNumber', ''),
            'username' : request.json.get('username', ''),
            'registered' : datetime.datetime.utcnow(),
            'isAdmin' : request.json.get('isAdmin', False)
        }
        if data['email'] == "keyerror":
            return "keyerror"
        self.db.append(data)
        return self.id

    def get_user(self, user_id):
        "Method to get a user"
        for user in self.db:
            if user['id'] == user_id:
                return user
        return "no user"

    def delete_user(self, user_id):
        "Method to delete a user"
        user = self.get_user(user_id)
        if user == "no user":
            return "no user"
        self.db.remove(user)
        return "deleted"

    def edit_user_location(self, user_id):
        "Method to edit a user's location"
        user = self.get_user(user_id)
        if user == "no user":
            return "no user"
        else:
            user['location'] = request.json.get('location', 'keyerror')
            if user['location'] == 'keyerror':
                return "keyerror"
            return "updated"

    def edit_user_comment(self, user_id):
        "Method to edit a user's comment"
        user = self.get_user(user_id)
        if user == "no user":
            return "no user"
        else:
            user['comment'] = request.json.get('comment', 'keyerror')
            if user['comment'] == 'keyerror':
                return "keyerror"
            return "updated"

    def edit_user(self, user_id):
        """Method to edit user fields"""
        user = self.get_user(user_id)
        if user == "no user":
            return "no user"
        user['firstname'] = request.json.get('firstname', user['firstname'])
        user['lastname'] = request.json.get('lastname', user['lastname'])
        user['othernames'] = request.json.get('status', user['othernames'])
        user['email'] = request.json.get('email', user['email'])
        user['phoneNumber'] = request.json.get('phoneNumber', user['phoneNumber'])
        user['username'] = request.json.get('username', user['username'])
        user['isAdmin'] = request.json.get('isAdmin', user['isAdmin'])

        return "updated"
        