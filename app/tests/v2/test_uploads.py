"""Tests for incident uploads run with pytest"""
import unittest
import json
import jwt
import datetime

from ... import create_app
from flask import current_app
from app.db_config import create_super_user, destroy_tables, create_tables
from app.tests.data import test_user, redflag_data, redflag_data2, redflag_data3
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

    def tearDown(self):
        url = self.APP.config.get('DATABASE_URL')
        destroy_tables(url)
