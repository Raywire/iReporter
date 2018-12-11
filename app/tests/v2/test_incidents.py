"""Tests for incidents run with pytest"""
import unittest
import json
import jwt
import datetime
import os

from ... import create_app
from app.db_config import create_test_user

APP = create_app()
create_test_user()
expiration_time = 10

secret_key = os.getenv('SECRET_KEY')


class IncidentTestCase(unittest.TestCase):
    """Class for testing incidents"""

    def setUp(self):
        """set up method initialising resused variables"""
        APP.testing = True
        self.app = APP.test_client()
        self.test_user = {
            "email": "ryanwire@outlook.com",
            "firstname": "Ryan1",
            "id": 4,
            "isAdmin": True,
            "lastname": "Wire",
            "othernames": "Simiyu",
            "password": "pbkdf2:sha256:50000$ziQztAJR$ea5d5a2cc01a0d919d60fe803ced2a8c8f0974f018607012f87802dc116f1ead",
            "phoneNumber": "0727272727",
            "public_id": "f3b8a1c3-f775-49e1-991c-5bfb963eb419",
            "registered": "Sat, 08 Dec 2018 08:34:45 GMT",
            "username": "ray"
        }
        token = jwt.encode({'public_id': self.test_user['public_id'], 'exp': datetime.datetime.utcnow(
        ) + datetime.timedelta(minutes=expiration_time)}, secret_key, algorithm='HS256')
        self.headers = {'Content-Type': 'application/json',
                        'x-access-token': token}
        self.headers_invalid = {
            'Content-Type': 'application/json', 'x-access-token': 'tokenisinvalid'}
        self.data = {
            "createdOn": "Tue, 27 Nov 2018 21:18:13 GMT",
            "createdBy": 1,
            'type': 'redflag',
            "location": "-90.000, -180.0000",
            "status": "draft",
            "images": "",
            "videos": "",
            "title": "Mercury in sugar",
            "comment": "Lorem ipsum dolor sit amet."
        }
        self.data2 = {
            "createdOn": "Tue, 27 Nov 2018 21:18:13 GMT",
            "createdByfhh": 2,
            'type': 'redflag',
            "location": "-90, -180",
            "status": "draft",
            "images": "",
            "videos": "",
            "title": "Mercury in sugar",
            "comment": "Lorem ipsum dolor sit amet."
        }
        self.data3 = {
            "createdOn": "Tue, 27 Nov 2018 21:18:13 GMT",
            'type': 'redflag',
            "location": "-90, -180",
            "status": "draft",
            "images": "",
            "videos": "",
            "comment": "Lorem ipsum dolor sit amet."
        }

    def test_get_all_redflags(self):
        """Test all redflags"""
        response = self.app.get("/api/v2/redflags", headers=self.headers)
        self.assertEqual(response.status_code, 200)

    def test_get_all_interventions(self):
        """Test all redflags"""
        response = self.app.get("/api/v2/interventions", headers=self.headers)
        self.assertEqual(response.status_code, 200)

    def test_get_all_redflags_no_token(self):
        """Test all redflags"""
        response = self.app.get("/api/v2/redflags")
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(result['message'], "Token is missing")

    def test_get_all_interventions_no_token(self):
        """Test all redflags"""
        response = self.app.get("/api/v2/interventions")
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(result['message'], "Token is missing")

    def test_get_all_redflags_invalid_token(self):
        """Test all redflags"""
        response = self.app.get(
            "/api/v2/redflags", headers=self.headers_invalid)
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(result['message'], "Token is invalid")

    def test_get_all_interventions_invalid_token(self):
        """Test all redflags"""
        response = self.app.get("/api/v2/interventions",
                                headers=self.headers_invalid)
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(result['message'], "Token is invalid")

    def test_wrong_status_key_redflag(self):
        """Test wrong status key used in redflag"""
        response = self.app.patch(
            "/api/v2/redflags/1/status", headers=self.headers, data=json.dumps({"status1": "draft  "}))
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(result['message']['status'],
                         "This key is required and should not be empty or formatted wrongly(Accepted values: draft, under investigatin, rejected, resolved)")

    def test_wrong_status_choice_in_redflag(self):
        """Test wrong status key used in redflag"""
        response = self.app.patch(
            "/api/v2/redflags/1/status", headers=self.headers, data=json.dumps({"status": "drafted"}))
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(result['message']['status'],
                         "This key is required and should not be empty or formatted wrongly(Accepted values: draft, under investigatin, rejected, resolved)")

    def test_wrong_comment_key_redflag(self):
        """Test wrong comment key used in redflag"""
        response = self.app.patch("/api/v2/redflags/1/comment", headers=self.headers,
                                  data=json.dumps({"comment1": "Cartels are taking over Kenya"}))
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(result['message']['comment'],
                         "This key is required and should not be empty or formatted wrongly")

    def test_wrong_location_key_redflag(self):
        """Test wrong location key used in redflag"""
        response = self.app.patch("/api/v2/redflags/1/location",
                                  headers=self.headers, data=json.dumps({"location1": "Nairobi"}))
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(result['message']['location'],
                         "This key is required and should not be empty or formatted wrongly")

    def test_wrong_status_key_intervention(self):
        """Test wrong status key used in intervention"""
        response = self.app.patch("/api/v2/interventions/1/status",
                                  headers=self.headers, data=json.dumps({"status1": "draft  "}))
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(result['message']['status'],
                         "This key is required and should not be empty or formatted wrongly(Accepted values: draft, under investigatin, rejected, resolved)")

    def test_wrong_status_choice_in_intervention(self):
        """Test wrong status key used in intervention"""
        response = self.app.patch("/api/v2/interventions/1/status",
                                  headers=self.headers, data=json.dumps({"status": "drafted"}))
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(result['message']['status'],
                         "This key is required and should not be empty or formatted wrongly(Accepted values: draft, under investigatin, rejected, resolved)")

    def test_wrong_comment_key_intervention(self):
        """Test wrong comment key used in intervention"""
        response = self.app.patch("/api/v2/interventions/1/comment", headers=self.headers,
                                  data=json.dumps({"comment1": "Cartels are taking over Kenya"}))
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(result['message']['comment'],
                         "This key is required and should not be empty or formatted wrongly")

    def test_wrong_location_key_intervention(self):
        """Test wrong location key used in intervention"""
        response = self.app.patch("/api/v2/interventions/1/location",
                                  headers=self.headers, data=json.dumps({"location1": "Nairobi"}))
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(result['message']['location'],
                         "This key is required and should not be empty or formatted wrongly")

    def test_redflag_not_found(self):
        """Test a redflag not found"""
        response = self.app.get("/api/v2/redflags/10000", headers=self.headers)
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(result['message'], "Redflag does not exist")

    def test_intervention_not_found(self):
        """Test a redflag not found"""
        response = self.app.get(
            "/api/v2/interventions/10000", headers=self.headers)
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(result['message'], "Intervention does not exist")

    def test_missing_key_redflag(self):
        """Test missing key in redflag"""
        response = self.app.post(
            "/api/v2/redflags", headers=self.headers, data=json.dumps(self.data3))
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 400)

    def test_missing_key_intervention(self):
        """Test missing key in redflag"""
        response = self.app.post(
            "/api/v2/interventions", headers=self.headers, data=json.dumps(self.data3))
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 400)

    def test_404_error(self):
        """Test for page not found"""
        response = self.app.get("/api/v2/interventinssdf")
        self.assertEqual(response.status_code, 404)
