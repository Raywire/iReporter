"""Tests for incident uploads run with pytest"""
import unittest
import json
import jwt
import datetime

from ... import create_app
from flask import current_app
from app.db_config import create_super_user, destroy_tables, create_tables
from app.tests.data import test_user, redflag_data, redflag_data2, redflag_data3, data, data5
from app.api.v2.send_email import send

expiration_time = 10


class IncidentUploadTestCase(unittest.TestCase):
    """Class for testing incident uploads"""

    def setUp(self):
        """set up method initialising resused variables"""
        self.APP = create_app(config_name="testing")
        self.app_context = self.APP.app_context()
        self.app_context.push()
        self.APP.testing = True
        self.app = self.APP.test_client()

        self.test_user = test_user
        self.data = data
        self.data5 = data5
        self.redflag_data = redflag_data
        token = jwt.encode({'public_id': self.test_user['public_id'], 'exp': datetime.datetime.utcnow(
        ) + datetime.timedelta(minutes=expiration_time)}, current_app.config['SECRET_KEY'], algorithm='HS256')
        self.headers = {'Content-Type': 'application/json',
                        'x-access-token': token}
        self.headers_invalid = {
            'Content-Type': 'application/json', 'x-access-token': 'tokenisinvalid'}

    def test_get_video(self):
        response = self.app.get(
            "/api/v2/uploads/videos/test_video.mp4", headers=self.headers)
        self.assertEqual(response.status_code, 200)

    def test_get_image(self):
        response = self.app.get(
            "/api/v2/uploads/images/test_image.jpg", headers=self.headers)
        self.assertEqual(response.status_code, 200)

    def test_upload_file_to_nonexistent_redflag(self):
        """Test to check upload image to redflag that does not exist"""
        response = self.app.patch("/api/v2/redflags/1/addImage", headers=self.headers)
        result2 = json.loads(response.data)
        self.assertEqual(result2['status'], 404)
        self.assertEqual(result2['message'], 'Redflag does not exist')

    def test_upload_with_no_file_to_redflag(self):
        """Test to check upload image to redflag with no file"""
        self.app.post(
            "/api/v2/redflags", headers=self.headers, data=json.dumps(self.redflag_data))
        response = self.app.patch("/api/v2/redflags/1/addImage", headers=self.headers)
        result2 = json.loads(response.data)
        self.assertEqual(result2['status'], 400)
        self.assertEqual(result2['message'], 'No uploadFile name in form')                           

    def test_upload_file_to_nonexistent_intervention(self):
        """Test to check upload image to intervention that does not exist"""
        response = self.app.patch("/api/v2/interventions/1/addImage", headers=self.headers)
        result2 = json.loads(response.data)
        self.assertEqual(result2['status'], 404)
        self.assertEqual(result2['message'], 'Intervention does not exist')

    def test_upload_with_no_file_to_intervention(self):
        """Test to check upload image to intervention with no file"""
        self.app.post(
            "/api/v2/interventions", headers=self.headers, data=json.dumps(self.redflag_data))
        response = self.app.patch("/api/v2/interventions/1/addImage", headers=self.headers)
        result2 = json.loads(response.data)
        self.assertEqual(result2['status'], 400)
        self.assertEqual(result2['message'], 'No uploadFile name in form') 

    def test_upload_profile_pic_with_no_file(self):
        """Test to check upload with no file selected"""
        self.app.post("/api/v2/auth/signup", headers=self.headers,
                      data=json.dumps(self.data))
        response = self.app.post(
            "/api/v2/auth/login", headers=self.headers, data=json.dumps(self.data5))
        result = json.loads(response.data)
        token = result['data'][0]['token']
        response2 = self.app.patch("/api/v2/users/jayd/uploadImage", headers={
                                   'Content-Type': 'application/json', 'x-access-token': token})
        result2 = json.loads(response2.data)
        self.assertEqual(result2['status'], 400)
        self.assertEqual(result2['message'], 'no file part')

    def test_upload_profile_pic_on_another_user(self):
        """Test to check if another user can upload a profile picture of another account"""
        self.app.post("/api/v2/auth/signup", headers=self.headers,
                      data=json.dumps(self.data))
        response = self.app.post(
            "/api/v2/auth/login", headers=self.headers, data=json.dumps(self.data5))
        result = json.loads(response.data)
        token = result['data'][0]['token']
        response2 = self.app.patch("/api/v2/users/jayd2/uploadImage", headers={
                                   'Content-Type': 'application/json', 'x-access-token': token},
                                   data=json.dumps({"file": "test.jpg"}))
        result2 = json.loads(response2.data)
        self.assertEqual(result2['status'], 403)
        self.assertEqual(result2['message'], 'A user can only upload a picture to their own profile')

    def tearDown(self):
        url = self.APP.config.get('DATABASE_URL')
        destroy_tables(url)
