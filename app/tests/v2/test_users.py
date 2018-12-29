"""Tests for users run with pytest"""
import unittest
import json
import jwt
import datetime
import os

from ... import create_app
from app.db_config import create_test_user, destroy_tables, create_tables
from app.tests.data import test_user, data, data2, data3, data4, data5, data6, data7


expiration_time = 10

secret_key = os.getenv('SECRET_KEY')

APP = create_app(config_name="testing")

class UserTestCase(unittest.TestCase):
    """Class for User testcase"""
    def setUp(self):
        """set up method initialising resused variables"""
        APP.testing = True
        self.app = APP.test_client()
        create_tables()
        create_test_user()
        self.test_user = test_user
        self.headers = {'Content-Type': 'application/json'}

        token = jwt.encode({'public_id': self.test_user['public_id'], 'exp': datetime.datetime.utcnow(
        ) + datetime.timedelta(minutes=expiration_time)}, secret_key, algorithm='HS256')
        self.headers_secured = {'Content-Type': 'application/json',
                        'x-access-token': token}
                            
        self.data = data
        self.data2 = data2
        self.data3 = data3
        self.data4 = data4
        self.data5 = data5
        self.data6 = data6
        self.data7 = data7

    def test_user_signup(self):
        """Test post a user signup"""       
        response = self.app.post("/api/v2/auth/signup", headers=self.headers, data=json.dumps(self.data))
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 200)

    def test_get_users(self):
        """Test to get all users"""       
        response = self.app.get("/api/v2/users", headers=self.headers_secured)
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 200)

    def test_get_specific_user(self):
        """Test get a specific redflag"""
        self.app.post("/api/v2/auth/signup", headers=self.headers_secured, data=json.dumps(self.data))
        response = self.app.get("/api/v2/users/jayd", headers=self.headers_secured)
        self.assertEqual(response.status_code, 200)

    def test_nonexistent_user(self):
        """Test to check a user who does not exist"""
        response = self.app.get("/api/v2/users/jayd", headers=self.headers_secured)
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.data)
        self.assertEqual(result['message'], 'user does not exist')    

    def test_delete_specific_user(self):
        """Test delete a specific redflag"""
        self.app.post("/api/v2/auth/signup", headers=self.headers_secured, data=json.dumps(self.data))
        response = self.app.delete("/api/v2/users/jayd", headers=self.headers_secured)
        self.assertEqual(response.status_code, 200)

    def test_update_user_status(self):
        """Test to update user admin status"""
        self.app.post("/api/v2/auth/signup", headers=self.headers_secured, data=json.dumps(self.data))
        response = self.app.patch("/api/v2/users/jayd/promote", headers=self.headers_secured, data=json.dumps({"isadmin":"False"}))
        self.assertEqual(response.status_code, 200)

    def test_user_signin(self):
        """Test post a user signin"""
        self.app.post("/api/v2/auth/signup", headers=self.headers, data=json.dumps(self.data))
        response = self.app.post("/api/v2/auth/login", headers=self.headers, data=json.dumps(self.data5))
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 200)       

    def test_user_signin_wrong_password(self):
        """Test post a user signin"""
        self.app.post("/api/v2/auth/signup", headers=self.headers, data=json.dumps(self.data))
        response = self.app.post("/api/v2/auth/login", headers=self.headers, data=json.dumps(self.data6))
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(result['message'], 'password or username is invalid')

    def test_user_signin_wrong_username(self):
        """Test post a user signin"""
        self.app.post("/api/v2/auth/signup", headers=self.headers, data=json.dumps(self.data))
        response = self.app.post("/api/v2/auth/login", headers=self.headers, data=json.dumps(self.data7))
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(result['message'], 'password or username is invalid')

    def test_duplicate_user_email(self):
        """Test post a user with existing email"""
        self.app.post("/api/v2/auth/signup", headers=self.headers, data=json.dumps(self.data))
        response = self.app.post("/api/v2/auth/signup", headers=self.headers, data=json.dumps(self.data))
        result = json.loads(response.data)
        self.assertEqual(result['status'], 400)
        self.assertEqual(result['message'], "email already exists")

    def test_duplicate_username(self):
        """Test post a user with existing username"""
        self.app.post("/api/v2/auth/signup", headers=self.headers, data=json.dumps(self.data3))
        response = self.app.post("/api/v2/auth/signup", headers=self.headers, data=json.dumps(self.data4))
        result = json.loads(response.data)
        self.assertEqual(result['status'], 400)
        self.assertEqual(result['message'], "username already exists")

    def test_wrong_key_in_post(self):
        """Tests for wrong key in user post request"""
        response = self.app.post("/api/v2/auth/signup", headers=self.headers, data=json.dumps(self.data2))
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 400)

    def tearDown(self):
        destroy_tables()                