"""User models"""
from werkzeug import generate_password_hash, check_password_hash
from app.db_config import connection, create_cursor
from flask import request
from flask_restful import reqparse

import datetime
import re
import uuid

url = "dbname='ireporter' host='localhost' port='5432' user='raywire' password='raywire2018'"
def validate_integers(value):
    """method to check for only integers"""
    if not re.match(r"^[0-9]+$", value):
        raise ValueError("Pattern not matched")
def validate_email(value):
    """method to check for valid coordinates"""
    if not re.match(r"^[^@]+@[^@]+\.[^@]+$", value):
        raise ValueError("Pattern not matched")
def validate_characters(value):
    """method to check if variable contains only characters"""
    if not re.match(r"^[a-zA-Z\d\-']+$", value):
        raise ValueError("Pattern not matched")    

parser = reqparse.RequestParser(bundle_errors=True)
parser_signin = reqparse.RequestParser(bundle_errors=True)

parser.add_argument('firstname',
                    type=validate_characters,
                    required=False,
                    nullable=False,
                    help="This key is required and should not be empty or formatted wrongly"
                    )

parser.add_argument('lastname',
                    type=validate_characters,
                    required=False,
                    nullable=False,
                    help="This key is required and should not be empty or formatted wrongly"
                    )

parser.add_argument('othernames',
                    type=validate_characters,
                    required=False,
                    nullable=False,
                    help="This key is required and should not be empty or formatted wrongly"
                    )

parser.add_argument('username',
                    type=validate_characters,
                    required=True,
                    nullable=True,
                    help="This key is required and should not be empty or formatted wrongly"
                    )

parser_signin.add_argument('username',
                    type=validate_characters,
                    required=True,
                    nullable=True,
                    help="This key is required and should not be empty or formatted wrongly"
                    )

parser.add_argument('email',
                    type=validate_email,
                    required=False,
                    nullable=True,
                    help="This key is required and should not be empty or formatted wrongly"
                    )

parser.add_argument('phoneNumber',
                    type=validate_integers,
                    required=False,
                    nullable=True,
                    help="This key is required and should not be empty or formatted wrongly"
                    )

parser.add_argument('password',
                    required=True,
                    nullable=False,
                    help="This key is required and should not be empty or formatted wrongly"
                    )

parser_signin.add_argument('password',
                    required=True,
                    nullable=False,
                    help="This key is required and should not be empty or formatted wrongly"
                    )

class UserModel:
    """User Model class with methods for manipulation user data"""
    def __init__(self):
        # self.firstname = firstname.title()
        # self.lastname = lastname.title()
        # self.othernames = othernames.title()
        # self.username = username
        # self.email = email.lower()
        # self.phoneNumber = phoneNumber
        self.registered = datetime.datetime.utcnow()
        # self.set_password(password)
        self.isAdmin = False
        self.public_id = str(uuid.uuid4())   
        self.db = connection(url)
        self.cursor = create_cursor(url)

    def set_password(self, password):
        return generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.pwdhash, password)

    def save_user(self):
        """method to add a user"""
        args = parser.parse_args()
        data = {
            'firstname' : request.json.get('firstname'),
            'lastname' : request.json.get('lastname'),
            'othernames' : request.json.get('othernames'),
            'email' : request.json.get('email'),
            'phoneNumber' : request.json.get('phoneNumber'),
            'username' : request.json.get('username'),
            'registered' : datetime.datetime.utcnow(),
            'password' : self.set_password(request.json.get('password')),
            'isAdmin' : self.isAdmin,
            'public_id' : self.public_id
        }
        userByEmail = self.get_user_by_email(data['email'])
        userByUsername = self.get_user_by_username(data['username'])
        if userByEmail != None:
            return 'email exists'
        elif userByUsername != None:
            return 'username exists'
        
        query = """INSERT INTO users (firstname,lastname,othernames,email,phoneNumber,username,registered,password,isAdmin,public_id) VALUES('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}',{8},'{9}');""".format(data['firstname'],data['lastname'],data['othernames'],data['email'],data['phoneNumber'],data['username'],data['registered'],data['password'],data['isAdmin'],data['public_id'])
        conn = self.db
        cursor = conn.cursor()
        cursor.execute(query)
        conn.commit()
        return data

    def get_user_by_email(self, email):
        "Method to get a user by username or email"
        query = """SELECT * from users WHERE email='{0}'""".format(email)
        self.cursor.execute(query)
        row = self.cursor.fetchall()

        if self.cursor.rowcount == 0:
            return None
        return row

    def get_user_by_username(self, username):
        "Method to get a user by username or email"
        query = """SELECT * from users WHERE username='{0}'""".format(username)
        self.cursor.execute(query)
        row = self.cursor.fetchone()

        if self.cursor.rowcount == 0:
            return None
        return row

    def sign_in(self):
        args = parser_signin.parse_args()
        data = {
            'username' : request.json.get('username'),
            'password' : request.json.get('password')
        }        
        user = self.get_user_by_username(data['username'])
        if user != None:
            user_data = {
                'id' : user['id'],
                'firstname' : user['firstname'],
                'lastname' : user['lastname'],
                'othernames' : user['othernames'],
                'email' : user['email'],
                'phoneNumber' : user['phonenumber'],
                'username' : user['username'],
                'registered' : user['registered'],
                'password' : user['password'],
                'isAdmin' : user['isadmin'],
                'public_id' : user['public_id']
            }

        if user == None:
            return None
        if check_password_hash(user_data['password'], data['password']) == False:
            return 'invalid password'
        return user_data


    def get_users(self):
        """method to get all users"""
        query = """SELECT * from users"""
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        return rows