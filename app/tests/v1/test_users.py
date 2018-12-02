"""Tests for users run with pytest"""
import unittest
import json

from ... import create_app

APP = create_app()

class UserTestCase(unittest.TestCase):
    """Class for User testcase"""
    def setUp(self):
        """set up method initialising resused variables"""
        APP.testing = True
        self.app = APP.test_client()
        self.data = {
            'id' : 1,
            'firstname' : "Ryan",
            'lastname' : "Wire",
            'othernames' : "Simiyu",
            'email' : "simiyuwire@gmail.com",
            'phoneNumber' : "+254724374281",
            'username' : "raywire",
            'registered' : "Tue, 27 Nov 2018 21:18:13 GMT",
            'password' : "123456",
            'isAdmin' : True
        }

        self.data2 = {
            'id' : 1,
            'firstname' : "Ryan",
            'lastname' : "Wire",
            'othernames' : "Simiyu",
            'emails' : "simiyuwire@gmail.com",
            'phoneNumber' : "+254724374281",
            'username' : "raywire",
            'registered' : "Tue, 27 Nov 2018 21:18:13 GMT",
            'password' : "123456",
            'isAdmin' : True
        }

        self.data3 = {
            'id' : 1,
            'firstname' : "Ryan",
            'lastname' : "Wire",
            'othernames' : "Simiyu",
            'email' : "rayosim09@gmail.com",
            'phoneNumber' : "+254724374281",
            'username' : "rayosim",
            'registered' : "Tue, 27 Nov 2018 21:18:13 GMT",
            'password' : "123456",
            'isAdmin' : True
        }

        self.data4 = {
            'id' : 1,
            'firstname' : "Ryan",
            'lastname' : "Wire",
            'othernames' : "Simiyu",
            'email' : "ryansimiyu@gmail.com",
            'phoneNumber' : "+254724374281",
            'username' : "rayosim",
            'registered' : "Tue, 27 Nov 2018 21:18:13 GMT",
            'password' : "123456",
            'isAdmin' : True
        }

    def test_get_all_users(self):
        """Test all users"""
        response = self.app.get("/api/v1/users")
        self.assertEqual(response.status_code, 200)

    def test_post_user(self):
        """Test post a user"""
        response = self.app.post("/api/v1/users", headers={'Content-Type': 'application/json'}, data=json.dumps(self.data3))
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(result['data']['message'], 'Created user record')

    def test_duplicate_user_email(self):
        """Test post a user with existing email"""
        self.app.post("/api/v1/users", headers={'Content-Type': 'application/json'}, data=json.dumps(self.data3))
        response = self.app.post("/api/v1/users", headers={'Content-Type': 'application/json'}, data=json.dumps(self.data3))
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(result['error'], 'email already exists')

    def test_duplicate_username(self):
        """Test post a user with existing username"""
        self.app.post("/api/v1/users", headers={'Content-Type': 'application/json'}, data=json.dumps(self.data3))
        response = self.app.post("/api/v1/users", headers={'Content-Type': 'application/json'}, data=json.dumps(self.data4))
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(result['error'], 'username already exists')

    def test_wrong_key_in_post(self):
        """Tests for wrong key in user post request"""
        response = self.app.post("/api/v1/users", headers={'Content-Type': 'application/json'}, data=json.dumps(self.data2))
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 500)
        self.assertEqual(result['error'], 'KeyError for email/password not posted')

    def test_get_specific_user(self):
        """Test get a specific user"""
        self.app.post("/api/v1/users", headers={'Content-Type': 'application/json'}, data=json.dumps(self.data))
        response = self.app.get("/api/v1/users/1")
        self.assertEqual(response.status_code, 200)

    def test_edit_specific_user(self):
        """Test to edit a specific redflag"""
        self.app.post("/api/v1/users", headers={'Content-Type': 'application/json'}, data=json.dumps(self.data))
        response = self.app.put("/api/v1/users/1", headers={'Content-Type': 'application/json'}, data=json.dumps(self.data))
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(result['data']['message'], "user record has been updated")  

    def test_update_status_of_user(self):
        """Test update status of a specific user"""
        response = self.app.patch("/api/v1/users/1/status", headers={'Content-Type': 'application/json'}, data=json.dumps({"isAdmin" : False}))
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(result['data']['message'], "Updated user's status")

    def test_update_password_of_user(self):
        """Test update password of a specific user"""
        response = self.app.patch("/api/v1/users/1/password", headers={'Content-Type': 'application/json'}, data=json.dumps({"password" : "Cartels"}))
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(result['data']['message'], "Updated user's password")

    def test_wrong_status_key(self):
        """Test wrong status key used in user"""
        response = self.app.patch("/api/v1/users/1/status", headers={'Content-Type': 'application/json'}, data=json.dumps({"isAdmina" : True}))
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 500)
        self.assertEqual(result['error'], "KeyError user's status not updated")

    def test_wrong_password_key(self):
        """Test wrong password key used in user"""
        response = self.app.patch("/api/v1/users/1/password", headers={'Content-Type': 'application/json'}, data=json.dumps({"password1" : "Nairobi"}))
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 500)
        self.assertEqual(result['error'], "KeyError user's password not updated")

    def test_delete_specific_user(self):
        """Test delete a specific user"""
        self.app.post("/api/v1/users", headers={'Content-Type': 'application/json'}, data=json.dumps(self.data))
        response = self.app.delete("/api/v1/users/1")
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(result['data']['message'], 'user record has been deleted')

    def test_user_not_found(self):
        """Test a user not found"""
        response = self.app.get("/api/v1/users/10")
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(result['error'], "user does not exist")
                