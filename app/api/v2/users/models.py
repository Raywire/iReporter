"""User models"""
from werkzeug import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from app.db_config import connection
from flask import request, current_app
from flask_restful import reqparse
from app.validators import (validate_username, validate_characters,
                            validate_email, validate_phonenumber,
                            validate_password, allowed_file)
from app.db_config import bucket
import psycopg2.extras

import datetime
import uuid

parser = reqparse.RequestParser(bundle_errors=True)
parser_signin = reqparse.RequestParser(bundle_errors=True)
parser_user = reqparse.RequestParser(bundle_errors=True)
parser_promote = reqparse.RequestParser(bundle_errors=True)
parser_activate = reqparse.RequestParser(bundle_errors=True)
parser_password = reqparse.RequestParser(bundle_errors=True)
parser_update = reqparse.RequestParser(bundle_errors=True)

parser.add_argument('firstname',
                    type=validate_characters, required=True, nullable=False,
                    help="This key is required and should not be empty or formatted wrongly"
                    )

parser.add_argument('lastname',
                    type=validate_characters, required=True, nullable=False,
                    help="This key is required and should not be empty or formatted wrongly"
                    )

parser.add_argument('othernames',
                    type=validate_characters, required=False, nullable=False,
                    help="This key is required and should not be empty or formatted wrongly"
                    )

parser.add_argument('username',
                    type=validate_username, required=True, nullable=False,
                    help="This key is required and should not be empty or formatted wrongly"
                    )

parser.add_argument('email',
                    type=validate_email, required=True, nullable=False,
                    help="This key is required and should not be empty or formatted wrongly"
                    )

parser.add_argument('phoneNumber',
                    type=validate_phonenumber, required=False, nullable=True,
                    help="This key is required and should not be empty or formatted wrongly"
                    )

parser.add_argument('password',
                    type=validate_password, required=True, nullable=False,
                    help="Password must be at least 6 characters"
                    )

parser_activate.add_argument('isactive', choices=["True", "False"],
                             required=True, nullable=False,
                             help="(Accepted values: True, False)"
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
            'firstname': request.json.get('firstname').capitalize(),
            'lastname': request.json.get('lastname').capitalize(),
            'othernames': request.json.get('othernames', '').capitalize(),
            'email': request.json.get('email').lower(),
            'phoneNumber': request.json.get('phoneNumber'),
            'username': request.json.get('username').lower(),
            'registered': datetime.datetime.utcnow(),
            'password': self.set_password(request.json.get('password')),
            'isAdmin': self.isAdmin, 'public_id': self.public_id
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
        query = """SELECT * from users WHERE public_id=%s OR username=%s OR email=%s"""
        user_value = value, value, value
        conn = self.db
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cursor.execute(query, user_value)
        row = cursor.fetchone()

        if cursor.rowcount == 0:
            return None
        return row

    def sign_in(self):
        parser_signin.add_argument('username', required=True,
                                   help="This key is required and should not be empty or formatted wrongly"
                                   )

        parser_signin.add_argument('password', required=True,
                                   help="This key is required and should not be empty or formatted wrongly"
                                   )

        args = parser_signin.parse_args()
        data = {
            'username': request.json.get('username').lower(),
            'password': request.json.get('password')
        }
        current_user = self.get_user(data['username'])
        if current_user is not None:
            current_user_data = {
                'email': current_user['email'],
                'emailVerified': current_user['emailverified'],
                'firstname': current_user['firstname'],
                'isActive': current_user['isactive'],
                'isAdmin': current_user['isadmin'],
                'lastname': current_user['lastname'],
                'othernames': current_user['othernames'],
                'phoneNumber': current_user['phonenumber'],
                'public_id': current_user['public_id'],
                'username': current_user['username'],
                'photourl': self.get_profile_picture_url(current_user['photourl'])
            }

        if current_user is None:
            return None
        if current_user['isactive'] is False:
            return 'disabled'
        if check_password_hash(current_user['password'], data['password']) is False:
            return False
        return current_user_data

    def get_users(self):
        """method to get all users"""
        query = """SELECT firstname,lastname,othernames,email,phonenumber,\
                    username,public_id,isadmin,isactive,registered\
                    from users ORDER BY registered ASC"""
        conn = self.db
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cursor.execute(query)
        rows = cursor.fetchall()
        return rows

    def promote_user(self, username):
        """method to upgrade a user to an admin user"""
        parser_promote.add_argument('isadmin', choices=["True", "False"],
                                    required=True, nullable=False,
                                    help="(Accepted values: True, False)"
                                    )
        args = parser_promote.parse_args()
        isAdmin = request.json.get('isadmin')

        query = """UPDATE users SET isadmin=%s WHERE username=%s"""
        values = isAdmin, username

        conn = self.db
        cursor = conn.cursor()
        cursor.execute(query, values)
        conn.commit()
        return True

    def activate_user(self, username):
        """method to disable or enable user activity"""
        args = parser_activate.parse_args()
        isActive = request.json.get('isactive')

        query = """UPDATE users SET isactive=%s WHERE username=%s"""
        values = isActive, username

        conn = self.db
        cursor = conn.cursor()
        cursor.execute(query, values)
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
        except psycopg2.IntegrityError:
            return False

    def update_user_password(self, username):
        """method to change a user's password"""
        parser_password.add_argument('password',
                                     type=validate_password, required=True,
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

    def update_user(self, username):
        """method to update a user's profile data"""
        parser_update.add_argument('email', type=validate_email,
                                   required=False, nullable=False,
                                   help="Email must be formatted correctly")

        parser_update.add_argument('phoneNumber', type=validate_phonenumber,
                                   required=False, nullable=False,
                                   help="Enter a valid phone number")

        parser_update.add_argument('firstname', type=validate_characters,
                                   required=False, nullable=False,
                                   help="First name must be formatted correctly")

        parser_update.add_argument('lastname', type=validate_characters,
                                   required=False, nullable=False,
                                   help="Last name must be formatted correctly")

        parser_update.add_argument('othernames', type=validate_characters,
                                   required=False, nullable=False,
                                   help="Other name must be formatted correctly")

        user = self.get_user(username)
        if user is None:
            return None

        args = parser_update.parse_args()
        new_data = {
            'email': request.json.get('email', user['email']).lower(),
            'firstname': request.json.get('firstname', user['firstname']).capitalize(),
            'lastname': request.json.get('lastname', user['lastname']).capitalize(),
            'othernames': request.json.get('othernames', user['othernames']).capitalize(),
            'phoneNumber': request.json.get('phoneNumber', user['phonenumber']),
        }

        getEmail = self.get_user(new_data['email'])
        verification_status = True

        if user['email'] != new_data['email']:
            if getEmail is not None:
                return 'email exists'
            verification_status = False

        query = """UPDATE users SET firstname=%s,lastname=%s,othernames=%s,\
                    email=%s,phonenumber=%s,emailverified=%s WHERE username=%s"""
        values = new_data['firstname'], new_data['lastname'], new_data['othernames'], new_data['email'], new_data['phoneNumber'], verification_status, username

        conn = self.db
        cursor = conn.cursor()
        cursor.execute(query, values)
        conn.commit()
        return new_data

    def upload_profile_pic(self, username):
        user = self.get_user(username)
        query = """UPDATE users SET photourl=%s WHERE username=%s"""
        if user is None:
            return None

        if 'file' not in request.files:
            return 'no file part'
        file = request.files['file']

        if file.filename == '':
            return 'select an image'
        if file and allowed_file(file.filename, 'images'):
            filename = secure_filename(file.filename)
            extension = filename.rsplit('.', 1)[1].lower()
            filename = str(username) + '.' + extension
            blob = bucket.blob('images/users/'+filename)
            blob.upload_from_file(file)
            values = filename, username
            conn = self.db
            cursor = conn.cursor()
            cursor.execute(query, values)
            conn.commit()
            return True
        return "File type not supported"

    @classmethod
    def get_profile_picture_url(cls, filename):
        """Get a user's profile picture"""
        if filename is None:
            return None
        profile_picture = bucket.blob('images/users/'+filename)
        if profile_picture.exists():
            profile_picture.make_public()
            return profile_picture.public_url
        return None

    def verify_user(self, username):
        query_verify = """UPDATE users SET emailverified=%s WHERE username=%s"""
        value = True, username
        connection_verify = self.db
        cursor_verify = connection_verify.cursor()
        cursor_verify.execute(query_verify, value)
        connection_verify.commit()
        return 'account verified'
