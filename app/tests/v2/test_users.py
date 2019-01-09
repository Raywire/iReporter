"""Tests for users run with pytest"""
import unittest
import json
import jwt
import datetime
import os

from ... import create_app
from flask import current_app
from app.db_config import (create_super_user, destroy_tables, create_tables)
from app.tests.data import (
    test_user, data, data2, data3, data4, data5, data6, data7,
    data8, redflag_data)


expiration_time = 10

test_email = os.getenv('SUPER_USER_EMAIL')


class UserTestCase(unittest.TestCase):
    """Class for User testcase"""

    def setUp(self):
        """set up method initialising resused variables"""
        self.APP = create_app(config_name="testing")
        self.app_context = self.APP.app_context()
        self.app_context.push()
        self.APP.testing = True
        self.app = self.APP.test_client()

        self.test_user = test_user
        self.data = data
        self.data2 = data2
        self.data3 = data3
        self.data4 = data4
        self.data5 = data5
        self.data6 = data6
        self.data7 = data7

        self.headers = {'Content-Type': 'application/json'}

        token = jwt.encode({'public_id': self.test_user['public_id'], 'exp': datetime.datetime.utcnow(
        ) + datetime.timedelta(minutes=expiration_time)}, current_app.config['SECRET_KEY'], algorithm='HS256')
        self.headers_secured = {'Content-Type': 'application/json',
                                'x-access-token': token}

    def test_user_signup(self):
        """Test post a user signup"""
        response = self.app.post(
            "/api/v2/auth/signup", headers=self.headers, data=json.dumps(self.data))
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 200)

    def test_get_users(self):
        """Test to get all users"""
        response = self.app.get("/api/v2/users", headers=self.headers_secured)
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 200)

    def test_get_users_none_admin(self):
        """Test for non admin trying to get all users"""

        response = self.app.post(
            "/api/v2/auth/signup", headers=self.headers, data=json.dumps(self.data))
        result = json.loads(response.data)
        token = result['data'][0]['token']
        response2 = self.app.get(
            "/api/v2/users", headers={'Content-Type': 'application/json', 'x-access-token': token})
        result2 = json.loads(response2.data)
        self.assertEqual(result2['status'], 403)
        self.assertEqual(result2['message'],
                         'Only admin can access this route')

    def test_get_specific_user(self):
        """Test get a specific redflag"""
        self.app.post("/api/v2/auth/signup",
                      headers=self.headers_secured, data=json.dumps(self.data))
        response = self.app.get("/api/v2/users/jayd",
                                headers=self.headers_secured)
        self.assertEqual(response.status_code, 200)

    def test_nonexistent_user(self):
        """Test to check a user who does not exist"""
        response = self.app.get("/api/v2/users/jayd",
                                headers=self.headers_secured)
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.data)
        self.assertEqual(result['message'], 'user does not exist')

    def test_delete_superadmin(self):
        """Test delete a specific redflag"""
        user = os.getenv('SUPER_USER_USERNAME')
        url = '/api/v2/users/' + user
        self.app.post("/api/v2/auth/signup", headers=self.headers_secured,
                      data=json.dumps(self.test_user))
        response = self.app.delete(url, headers=self.headers_secured)
        result = json.loads(response.data)
        self.assertEqual(result['message'], 'You cannot delete this user')
        self.assertEqual(result['status'], 403)

    def test_delete_nonexistent_user(self):
        """Test delete a specific redflag"""
        response = self.app.delete(
            "/api/v2/users/jayd1", headers=self.headers_secured)
        result = json.loads(response.data)
        self.assertEqual(result['message'], 'user does not exist')
        self.assertEqual(result['status'], 404)

    def test_delete_user(self):
        """Test delete a specific redflag"""
        self.app.post("/api/v2/auth/signup",
                      headers=self.headers_secured, data=json.dumps(self.data))
        response = self.app.delete(
            "/api/v2/users/jayd", headers=self.headers_secured)
        result = json.loads(response.data)
        self.assertEqual(result['data']['message'],
                         'user record has been deleted')
        self.assertEqual(response.status_code, 200)

    def test_delete_user_none_admin(self):
        """Test for none admin trying to delete a user"""
        response = self.app.post(
            "/api/v2/auth/signup", headers=self.headers, data=json.dumps(self.data))
        result = json.loads(response.data)
        response2 = self.app.delete("/api/v2/users/jayd", headers={
                                    'Content-Type': 'application/json',
                                    'x-access-token': result['data'][0]['token']})
        result2 = json.loads(response2.data)
        self.assertEqual(result2['status'], 403)
        self.assertEqual(result2['message'], 'You cannot delete this user')

    def test_delete_yourself(self):
        """Test for an admin user trying to delete themself"""
        self.app.post("/api/v2/auth/signup", headers=self.headers,
                      data=json.dumps(self.data))
        self.app.patch("/api/v2/users/jayd/promote",
                       headers=self.headers_secured, data=json.dumps({"isadmin": "True"}))
        response = self.app.post(
            "/api/v2/auth/login", headers=self.headers, data=json.dumps(self.data5))
        result = json.loads(response.data)
        token = result['data'][0]['token']
        response2 = self.app.delete(
            "/api/v2/users/jayd", headers={'Content-Type': 'application/json',
            'x-access-token': token})
        result2 = json.loads(response2.data)
        self.assertEqual(result2['status'], 403)
        self.assertEqual(result2['message'], 'You cannot delete this user')

    def test_delete_user_with_incident(self):
        """Test for an admin user trying to delete a user who has incidents"""
        self.app.post("/api/v2/auth/signup", headers=self.headers,
                      data=json.dumps(self.data))
        self.app.patch("/api/v2/users/jayd/promote",
                       headers=self.headers_secured, data=json.dumps({"isadmin": "True"}))
        response = self.app.post(
            "/api/v2/auth/login", headers=self.headers, data=json.dumps(self.data5))
        result = json.loads(response.data)
        token = result['data'][0]['token']
        self.app.post(
            "/api/v2/redflags", headers={'Content-Type': 'application/json',
            'x-access-token': token}, data=json.dumps(redflag_data))
        response2 = self.app.delete(
            "/api/v2/users/jayd", headers=self.headers_secured)
        result2 = json.loads(response2.data)
        self.assertEqual(result2['status'], 400)
        self.assertEqual(
            result2['message'], 'A user who has posted incidents cannot be deleted')

    def test_update_user_status(self):
        """Test to update user admin status"""
        self.app.post("/api/v2/auth/signup",
                      headers=self.headers_secured, data=json.dumps(self.data))
        response = self.app.patch("/api/v2/users/jayd/promote",
                                  headers=self.headers_secured, data=json.dumps({"isadmin": "False"}))
        self.assertEqual(response.status_code, 200)

    def test_user_signin(self):
        """Test post a user signin"""
        self.app.post("/api/v2/auth/signup", headers=self.headers,
                      data=json.dumps(self.data))
        response = self.app.post(
            "/api/v2/auth/login", headers=self.headers, data=json.dumps(self.data5))
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 200)

    def test_user_signin_wrong_password(self):
        """Test post a user signin"""
        self.app.post("/api/v2/auth/signup", headers=self.headers,
                      data=json.dumps(self.data))
        response = self.app.post(
            "/api/v2/auth/login", headers=self.headers, data=json.dumps(self.data6))
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(result['message'], 'password or username is invalid')

    def test_user_signin_wrong_username(self):
        """Test post a user signin"""
        self.app.post("/api/v2/auth/signup", headers=self.headers,
                      data=json.dumps(self.data))
        response = self.app.post(
            "/api/v2/auth/login", headers=self.headers, data=json.dumps(self.data7))
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(result['message'], 'password or username is invalid')

    def test_duplicate_user_email(self):
        """Test post a user with existing email"""
        self.app.post("/api/v2/auth/signup", headers=self.headers,
                      data=json.dumps(self.data))
        response = self.app.post(
            "/api/v2/auth/signup", headers=self.headers, data=json.dumps(self.data))
        result = json.loads(response.data)
        self.assertEqual(result['status'], 400)
        self.assertEqual(result['message'], "email already exists")

    def test_duplicate_username(self):
        """Test post a user with existing username"""
        self.app.post("/api/v2/auth/signup", headers=self.headers,
                      data=json.dumps(self.data3))
        response = self.app.post(
            "/api/v2/auth/signup", headers=self.headers, data=json.dumps(self.data4))
        result = json.loads(response.data)
        self.assertEqual(result['status'], 400)
        self.assertEqual(result['message'], "username already exists")

    def test_wrong_key_in_post(self):
        """Tests for wrong key in user post request"""
        response = self.app.post(
            "/api/v2/auth/signup", headers=self.headers, data=json.dumps(self.data2))
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 400)

    def test_promote_super_user(self):
        """Test to promote user"""
        self.app.post("/api/v2/auth/signup",
                      headers=self.headers_secured, data=json.dumps(self.data))
        response = self.app.patch("/api/v2/users/jayd/promote",
                                  headers=self.headers_secured, data=json.dumps({"isadmin": "True"}))
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(result['data']['message'],
                         "User status has been updated")

    def test_admin_update_user_password(self):
        """Tests user password change"""
        self.app.post("/api/v2/auth/signup",
                      headers=self.headers_secured, data=json.dumps(self.data))
        response = self.app.patch(
            "/api/v2/users/jayd", headers=self.headers_secured, data=json.dumps({"password": "123457"}))
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(result['message'], "User password has been changed")

    def test_update_user_password(self):
        """Test for a user updating their own password"""

        self.app.post("/api/v2/auth/signup", headers=self.headers,
                      data=json.dumps(self.data))
        response = self.app.post(
            "/api/v2/auth/login", headers=self.headers, data=json.dumps(self.data5))
        result = json.loads(response.data)
        token = result['data'][0]['token']
        response2 = self.app.patch("/api/v2/users/jayd", headers={
                                   'Content-Type': 'application/json', 'x-access-token': token},
                                   data=json.dumps({"password": "123457"}))
        result2 = json.loads(response2.data)
        self.assertEqual(result2['status'], 200)
        self.assertEqual(result2['message'], 'User password has been changed')

    def test_none_admin_update_another_user_password(self):
        """Test for a none admin user trying to update another user's password"""

        self.app.post("/api/v2/auth/signup", headers=self.headers,
                      data=json.dumps(self.data))
        self.app.post("/api/v2/auth/signup", headers=self.headers,
                      data=json.dumps(self.data3))
        response = self.app.post("/api/v2/auth/login",
                                 headers=self.headers, data=json.dumps(data8))
        result = json.loads(response.data)
        token = result['data'][0]['token']
        response2 = self.app.patch("/api/v2/users/jayd", headers={
                                   'Content-Type': 'application/json', 'x-access-token': token},
                                   data=json.dumps({"password": "123457"}))
        result2 = json.loads(response2.data)
        self.assertEqual(
            result2['message'], 'Only an admin or the user can update their own password')
        self.assertEqual(result2['status'], 403)

    def test_user_reset_password(self):
        """Test to check if reset password link is sent"""
        reset_link = "/api/v2/users/" + test_email + "/resetPassword"
        response = self.app.post(reset_link, headers=self.headers, data=json.dumps(
            {"resetlink": "https://yourdomain.com/reset_password.html"}))
        result = json.loads(response.data)
        self.assertEqual(result['message'],
                         'Reset link has been sent to your email')

    def tearDown(self):
        url = self.APP.config.get('DATABASE_URL')
        destroy_tables(url)
