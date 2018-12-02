"""User Models"""
import datetime
from flask import request
from werkzeug import generate_password_hash, check_password_hash

USERS = []

class UserModel:
    """user model class"""
    def __init__(self):
        self.db = USERS
        if not self.db:
            self.id = 1
        else:
            self.id = self.db[-1]['id'] + 1

    def set_password(self, password):
        """method for hashing password"""
        self.pwdhash = generate_password_hash(password)

    def check_password(self, password):
        """method for checking hashed password"""
        return check_password_hash(self.pwdhash, password)

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
            'password' : request.json.get('password','keyerror'),
            'isAdmin' : request.json.get('isAdmin', False)
        }
        if data['email'] == "keyerror" or data['password'] == "keyerror":
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

    def edit_user_status(self, user_id):
        "Method to edit a user's status"
        user = self.get_user(user_id)
        if user == "no user":
            return "no user"
        else:
            user['isAdmin'] = request.json.get('isAdmin', 'keyerror')
            if user['isAdmin'] == 'keyerror':
                return "keyerror"
            return "updated"

    def edit_user_password(self, user_id):
        "Method to edit a user's comment"
        user = self.get_user(user_id)
        if user == "no user":
            return "no user"
        else:
            user['password'] = request.json.get('password', 'keyerror')
            if user['password'] == 'keyerror':
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
        user['password'] = request.json.get('password', user['password'])
        user['isAdmin'] = request.json.get('isAdmin', user['isAdmin'])

        return "updated"
        