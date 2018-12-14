"""Tests for users run with pytest"""
import unittest
import json

from ... import create_app
from app.db_config import create_super_user, destroy_tables, create_tables
from app.tests.data import data, data2, data3, data4, data5

APP = create_app(config_name="testing")

class UserTestCase(unittest.TestCase):
    """Class for User testcase"""
    def setUp(self):
        """set up method initialising resused variables"""
        APP.testing = True
        self.app = APP.test_client()
        create_tables()
        create_super_user()
        self.headers = {'Content-Type': 'application/json'}        
        self.data = data
        self.data2 = data2
        self.data3 = data3
        self.data4 = data4
        self.data5 = data5

    def test_user_signup(self):
        """Test post a user signup"""       
        response = self.app.post("/api/v2/auth/signup", headers=self.headers, data=json.dumps(self.data))
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 200)

    def test_user_signin(self):
        """Test post a user signin"""
        self.app.post("/api/v2/auth/signup", headers=self.headers, data=json.dumps(self.data))
        response = self.app.post("/api/v2/auth/login", headers=self.headers, data=json.dumps(self.data5))
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 200)       

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