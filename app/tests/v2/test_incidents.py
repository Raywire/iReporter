"""Tests for incidents run with pytest"""
import unittest
import json
import jwt
import datetime
import os

from ... import create_app
from app.db_config import create_super_user, destroy_tables, create_tables
from app.tests.data import test_user, redflag_data, redflag_data2, redflag_data3

APP = create_app(config_name="testing")

expiration_time = 10

secret_key = os.getenv('SECRET_KEY')


class IncidentTestCase(unittest.TestCase):
    """Class for testing incidents"""

    def setUp(self):
        """set up method initialising resused variables"""
        APP.testing = True
        self.app = APP.test_client()
        create_tables()
        create_super_user()
        self.test_user = test_user
        token = jwt.encode({'public_id': self.test_user['public_id'], 'exp': datetime.datetime.utcnow(
        ) + datetime.timedelta(minutes=expiration_time)}, secret_key, algorithm='HS256')
        self.headers = {'Content-Type': 'application/json',
                        'x-access-token': token}
        self.headers_invalid = {
            'Content-Type': 'application/json', 'x-access-token': 'tokenisinvalid'}
        self.redflag_data = redflag_data
        self.redflag_data2 = redflag_data2
        self.redflag_data3 = redflag_data3

    def test_get_all_redflags(self):
        """Test all redflags"""
        response = self.app.get("/api/v2/redflags", headers=self.headers)
        self.assertEqual(response.status_code, 200)

    def test_get_all_interventions(self):
        """Test all redflags"""
        response = self.app.get("/api/v2/interventions", headers=self.headers)
        self.assertEqual(response.status_code, 200)

    def test_get_specific_redflag(self):
        """Test get a specific redflag"""
        self.app.post("/api/v2/redflags", headers=self.headers, data=json.dumps(self.redflag_data))
        response = self.app.get("/api/v2/redflags/1", headers=self.headers)
        self.assertEqual(response.status_code, 200)

    def test_get_specific_intervention(self):
        """Test get a specific intervention"""
        self.app.post("/api/v2/interventions", headers=self.headers, data=json.dumps(self.redflag_data))
        response = self.app.get("/api/v2/interventions/1", headers=self.headers)
        self.assertEqual(response.status_code, 200)

    def test_post_redflag(self):
        """Test post a redflag"""
        response = self.app.post("/api/v2/redflags", headers=self.headers, data=json.dumps(self.redflag_data))
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(result['status'], 201)           

    def test_post_intervention(self):
        """Test post a intervention"""
        response = self.app.post("/api/v2/interventions", headers=self.headers, data=json.dumps(self.redflag_data))
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(result['status'], 201)

    def test_update_status_of_redflag(self):
        """Test update status of a specific redflag"""
        response = self.app.patch("/api/v2/redflags/1/status", headers=self.headers, data=json.dumps({"status" : "resolved"}))
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 200)

    def test_update_location_of_redflag(self):
        """Test update location of a specific redflag"""
        response = self.app.patch("/api/v2/redflags/1/location", headers=self.headers, data=json.dumps({"location" : "-75.0, -12.554334"}))
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 200)

    def test_update_comment_of_redflag(self):
        """Test update comment of a specific redflag"""
        response = self.app.patch("/api/v2/redflags/1/comment", headers=self.headers, data=json.dumps({"comment" : "Cartels are taking over Kenya"}))
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 200)        

    def test_update_status_of_intervention(self):
        """Test update status of a specific intervention"""
        response = self.app.patch("/api/v2/interventions/1/status", headers=self.headers, data=json.dumps({"status" : "resolved"}))
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 200)

    def test_update_location_of_intervention(self):
        """Test update location of a specific intervention"""
        response = self.app.patch("/api/v2/interventions/1/location", headers=self.headers, data=json.dumps({"location" : "-75.0, -12.554334"}))
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 200)

    def test_update_comment_of_intervention(self):
        """Test update comment of a specific intervention"""
        response = self.app.patch("/api/v2/interventions/1/comment", headers=self.headers, data=json.dumps({"comment" : "Cartels are taking over Kenya"}))
        result = json.loads(response.data)
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
        self.assertEqual(result['message'],
                         "Input payload validation failed")

    def test_wrong_status_choice_in_redflag(self):
        """Test wrong status key used in redflag"""
        response = self.app.patch(
            "/api/v2/redflags/1/status", headers=self.headers, data=json.dumps({"status": "drafted"}))
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(result['message'],
                         "Input payload validation failed")

    def test_wrong_comment_key_redflag(self):
        """Test wrong comment key used in redflag"""
        response = self.app.patch("/api/v2/redflags/1/comment", headers=self.headers,
                                  data=json.dumps({"comment1": "Cartels are taking over Kenya"}))
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(result['message'],
                         "Input payload validation failed")

    def test_wrong_location_key_redflag(self):
        """Test wrong location key used in redflag"""
        response = self.app.patch("/api/v2/redflags/1/location",
                                  headers=self.headers, data=json.dumps({"location1": "Nairobi"}))
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(result['message'],
                         "Input payload validation failed")

    def test_wrong_status_key_intervention(self):
        """Test wrong status key used in intervention"""
        response = self.app.patch("/api/v2/interventions/1/status",
                                  headers=self.headers, data=json.dumps({"status1": "draft  "}))
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(result['message'],
                         "Input payload validation failed")

    def test_wrong_status_choice_in_intervention(self):
        """Test wrong status key used in intervention"""
        response = self.app.patch("/api/v2/interventions/1/status",
                                  headers=self.headers, data=json.dumps({"status": "drafted"}))
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(result['message'],
                         "Input payload validation failed")

    def test_wrong_comment_key_intervention(self):
        """Test wrong comment key used in intervention"""
        response = self.app.patch("/api/v2/interventions/1/comment", headers=self.headers,
                                  data=json.dumps({"comment1": "Cartels are taking over Kenya"}))
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(result['message'],
                         "Input payload validation failed")

    def test_wrong_location_key_intervention(self):
        """Test wrong location key used in intervention"""
        response = self.app.patch("/api/v2/interventions/1/location",
                                  headers=self.headers, data=json.dumps({"location1": "Nairobi"}))
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(result['message'],
                         "Input payload validation failed")

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
            "/api/v2/redflags", headers=self.headers, data=json.dumps(self.redflag_data3))
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 400)

    def test_missing_key_intervention(self):
        """Test missing key in redflag"""
        response = self.app.post(
            "/api/v2/interventions", headers=self.headers, data=json.dumps(self.redflag_data3))
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 400)

    def test_delete_specific_redflag(self):
        """Test delete a specific redflag"""
        self.app.post("/api/v2/redflags", headers=self.headers, data=json.dumps(self.redflag_data))
        response = self.app.delete("/api/v2/redflags/1", headers=self.headers)
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(result['data']['message'], 'Redflag record has been deleted')        

    def test_delete_nonexistent_redflag(self):
        """Test delete a nonexistent redflag"""
        self.app.post("/api/v2/redflags", headers=self.headers, data=json.dumps(self.redflag_data))
        response = self.app.delete("/api/v2/redflags/1000", headers=self.headers)
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(result['message'], 'Redflag does not exist')

    def test_delete_specific_intervention(self):
        """Test delete a specific intervention"""
        self.app.post("/api/v2/interventions", headers=self.headers, data=json.dumps(self.redflag_data))
        response = self.app.delete("/api/v2/interventions/1", headers=self.headers)
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(result['data']['message'], 'Intervention record has been deleted')        

    def test_delete_nonexistent_intervention(self):
        """Test delete a nonexistent intervention"""
        self.app.post("/api/v2/interventions", headers=self.headers, data=json.dumps(self.redflag_data))
        response = self.app.delete("/api/v2/interventions/10000", headers=self.headers)
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(result['message'], 'Intervention does not exist')

    def test_404_error(self):
        """Test for page not found"""
        response = self.app.get("/api/v2/interventinssdf")
        self.assertEqual(response.status_code, 404)

    def tearDown(self):
        destroy_tables()
