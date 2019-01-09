"""User models"""
from werkzeug import generate_password_hash, check_password_hash
from app.db_config import connection, init_database
from flask import request, current_app
from flask_restful import reqparse
from app.validators import (validate_username,validate_characters,
                            validate_email, validate_integers,
                            validate_password)
import psycopg2.extras

import datetime
import re
import uuid
import os

parser = reqparse.RequestParser(bundle_errors=True)
parser_signin = reqparse.RequestParser(bundle_errors=True)
parser_user = reqparse.RequestParser(bundle_errors=True)
parser_promote = reqparse.RequestParser(bundle_errors=True)
parser_password = reqparse.RequestParser(bundle_errors=True)

parser.add_argument('firstname',
                    type=validate_characters,
                    required=True,
                    nullable=False,
                    help="This key is required and should not be empty or formatted wrongly"
                    )

parser.add_argument('lastname',
                    type=validate_characters,
                    required=True,
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
                    type=validate_username,
                    required=True,
                    nullable=False,
                    help="This key is required and should not be empty or formatted wrongly"
                    )

parser.add_argument('email',
                    type=validate_email,
                    required=True,
                    nullable=False,
                    help="This key is required and should not be empty or formatted wrongly"
                    )

parser.add_argument('phoneNumber',
                    type=validate_integers,
                    required=False,
                    nullable=True,
                    help="This key is required and should not be empty or formatted wrongly"
                    )

parser.add_argument('password',
                    type=validate_password,
                    required=True,
                    nullable=False,
                    help="Password must be at least 6 characters"
                    )


class UserModel:
    """User Model class with methods for manipulation user data"""

    def __init__(self):
        self.registered = datetime.datetime.utcnow()
        self.isAdmin = False
        self.public_id = str(uuid.uuid4())
        url = current_app.config.get('DATABASE_URL')
        self.db = connection(url)

    def set_password(self, password):
        return generate_password_hash(password)

    def save_user(self):
        """method to add a user"""
        args = parser.parse_args()
        data = {
            'firstname': request.json.get('firstname').title(),
            'lastname': request.json.get('lastname').title(),
            'othernames': request.json.get('othernames', '').title(),
            'email': request.json.get('email').lower(),
            'phoneNumber': request.json.get('phoneNumber'),
            'username': request.json.get('username').lower(),
            'registered': datetime.datetime.utcnow(),
            'password': self.set_password(request.json.get('password')),
            'isAdmin': self.isAdmin,
            'public_id': self.public_id
        }
        userByEmail = self.get_user(data['email'])
        userByUsername = self.get_user(data['username'])
        if userByEmail is not None:
            return 'email exists'
        elif userByUsername is not None:
            return 'username exists'

        query = """INSERT INTO users (firstname,lastname,othernames,email,phoneNumber,username,registered,password,isAdmin,public_id) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
        values = data['firstname'], data['lastname'], data['othernames'], data['email'], data['phoneNumber'], data[
            'username'], data['registered'], data['password'], data['isAdmin'], data['public_id']

        conn = self.db
        cursor = conn.cursor()
        cursor.execute(query, values)
        conn.commit()
        return data

    def get_user(self, value):
        "Method to get a user by username or public_id"
        query = """SELECT * from users WHERE public_id='{0}' OR username='{0}' OR email='{0}'""".format(
            value)
        conn = self.db
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cursor.execute(query)
        row = cursor.fetchone()

        if cursor.rowcount == 0:
            return None
        return row

    def sign_in(self):
        parser_signin.add_argument('username',
                                   required=True,
                                   help="This key is required and should not be empty or formatted wrongly"
                                   )

        parser_signin.add_argument('password',
                                   required=True,
                                   help="This key is required and should not be empty or formatted wrongly"
                                   )

        args = parser_signin.parse_args()
        data = {
            'username': request.json.get('username'),
            'password': request.json.get('password')
        }
        user = self.get_user(data['username'])
        if user is not None:
            user_data = {
                'id': user['id'],
                'firstname': user['firstname'],
                'lastname': user['lastname'],
                'othernames': user['othernames'],
                'email': user['email'],
                'phoneNumber': user['phonenumber'],
                'username': user['username'],
                'public_id': user['public_id'],
                'isAdmin': user['isadmin']
            }

        if user is None:
            return None
        if check_password_hash(user['password'], data['password']) is False:
            return False
        return user_data

    def get_users(self):
        """method to get all users"""
        query = """SELECT firstname,lastname,othernames,email,phonenumber,\
                    username,public_id,isadmin,registered\
                    from users ORDER BY registered ASC"""
        conn = self.db
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cursor.execute(query)
        rows = cursor.fetchall()
        return rows

    def promote_user(self, username):
        """method to upgrade a user to an admin user"""
        parser_promote.add_argument('isadmin',
                                    choices=["True", "False"],
                                    required=True,
                                    nullable=False,
                                    help="(Accepted values: True, False)"
                                    )
        args = parser_promote.parse_args()
        isAdmin = request.json.get('isadmin')

        query = """UPDATE users SET isadmin='{0}' WHERE username='{1}'""".format(
            isAdmin, username)

        conn = self.db
        cursor = conn.cursor()
        cursor.execute(query)
        conn.commit()
        return True

    def delete_user(self, username):
        """method to delete a user"""
        try:
            conn = self.db
            cursor = conn.cursor()
            cursor.execute(
                """DELETE FROM users WHERE username='{0}'""".format(username))
            conn.commit()
            return True
        except:
            return False

    def update_user_password(self, username):
        """method to change a user's password"""
        parser_password.add_argument('password',
                                     type=validate_password,
                                     required=True,
                                     nullable=False,
                                     help="Password must be at least 6 characters"
                                     )
        args = parser_password.parse_args()
        password = self.set_password(request.json.get('password'))

        query = """UPDATE users SET password=%s WHERE username=%s"""
        values = password, username

        conn = self.db
        cursor = conn.cursor()
        cursor.execute(query, values)
        conn.commit()
        return True
