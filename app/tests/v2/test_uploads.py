"""Tests for incident uploads run with pytest"""
import unittest
import json
import jwt
import datetime
import os

from ... import create_app
from app.db_config import create_super_user, destroy_tables, create_tables
from app.tests.data import test_user, redflag_data, redflag_data2, redflag_data3
from app.api.v2.send_email import send

APP = create_app(config_name="testing")

expiration_time = 10

secret_key = os.getenv('SECRET_KEY')

class IncidentUploadTestCase(unittest.TestCase):
    """Class for testing incident uploads"""

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

    def test_nonexistent_image(self):
        response = self.app.get("/api/v2/uploads/images/154614577211.jpg", headers=self.headers)
        result = json.loads(response.data)
        self.assertEqual(result['status'], 404)
        self.assertEqual(result['message'], 'Image does not exist')
        
    def test_nonexistent_video(self):
        response = self.app.get("/api/v2/uploads/videos/154614577211.mp4", headers=self.headers)
        result = json.loads(response.data)
        self.assertEqual(result['status'], 404)
        self.assertEqual(result['message'], 'Video does not exist')

    # def test_get_video(self):
    #     response = self.app.get("/api/v2/uploads/videos/test_video.mp4", headers=self.headers)
    #     result = json.loads(response.data)
    #     self.assertEqual(result, 404)      

    # def test_get_image(self):
    #     response = self.app.get("/api/v2/uploads/images/test_image.jpg", headers=self.headers)
    #     result = json.loads(response.data)
    #     self.assertEqual(result, 404)

    def tearDown(self):
        destroy_tables()        