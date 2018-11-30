"""Tests for redflags run with pylint"""
import unittest
import json

from ... import create_app

APP = create_app()

class RedFlagTestCase(unittest.TestCase):
    """Class for Red-flags"""
    def setUp(self):
        """set up method initialising resused variables"""
        APP.testing = True
        self.app = APP.test_client()
        self.data = {
            "id": 1,
            "createdOn" : "Tue, 27 Nov 2018 21:18:13 GMT",
            "createdBy" : "Admin",
            'type' : 'red-flags',
            "location" : "Nakuru",
            "status" : "draft",
            "images" : "",
            "videos" : "",
            "title" : "Mercury in sugar",
            "comment" : "Lorem ipsum dolor sit amet."
        }
        self.data2 = {
            "id": 1,
            "createdOn" : "Tue, 27 Nov 2018 21:18:13 GMT",
            "createdByfhh" : "Admin",
            'type' : 'red-flags',
            "location" : "Nakuru",
            "status" : "draft",
            "images" : "",
            "videos" : "",
            "title" : "Mercury in sugar",
            "comment" : "Lorem ipsum dolor sit amet."
        }

    def test_get_all_redflags(self):
        """Test all redflags"""
        response = self.app.get("/api/v1/red-flags")
        self.assertEqual(response.status_code, 200)

    def test_post_redflag(self):
        """Test post a redflag"""
        response = self.app.post("/api/v1/red-flags", headers={'Content-Type': 'application/json'}, data=json.dumps(self.data))
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(result['data']['message'], 'Created red-flag record')

    def test_wrong_key_in_post(self):
        """Tests for wrong key in redflag post request"""
        response = self.app.post("/api/v1/red-flags", headers={'Content-Type': 'application/json'}, data=json.dumps(self.data2))
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 500)
        self.assertEqual(result['error'], 'KeyError for createdBy Red-flag not posted')

    def test_get_specific_redflag(self):
        """Test get a specific redflag"""
        self.app.post("/api/v1/red-flags", headers={'Content-Type': 'application/json'}, data=json.dumps(self.data))
        response = self.app.get("/api/v1/red-flags/1")
        self.assertEqual(response.status_code, 200)

    def test_update_location_of_redflag(self):
        """Test update location of a specific redflag"""
        response = self.app.patch("/api/v1/red-flags/1/location", headers={'Content-Type': 'application/json'}, data=json.dumps({"location" : "Nairobi"}))
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(result['data']['message'], "Updated red-flag record's location")

    def test_update_comment_of_redflag(self):
        """Test update comment of a specific redflag"""
        response = self.app.patch("/api/v1/red-flags/1/comment", headers={'Content-Type': 'application/json'}, data=json.dumps({"comment" : "Cartels are taking over Kenya"}))
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(result['data']['message'], "Updated red-flag record's comment")

    def test_wrong_comment_key(self):
        """Test wrong comment key used in redflag"""
        response = self.app.patch("/api/v1/red-flags/1/comment", headers={'Content-Type': 'application/json'}, data=json.dumps({"comment1" : "Cartels are taking over Kenya"}))
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 500)
        self.assertEqual(result['error'], "KeyError Red-flag's comment not updated")

    def test_wrong_location_key(self):
        """Test wrong location key used in redflag"""
        response = self.app.patch("/api/v1/red-flags/1/location", headers={'Content-Type': 'application/json'}, data=json.dumps({"location1" : "Nairobi"}))
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 500)
        self.assertEqual(result['error'], "KeyError Red-flag's location not updated")

    def test_delete_specific_redflag(self):
        """Test delete a specific redflag"""
        self.app.post("/api/v1/red-flags", headers={'Content-Type': 'application/json'}, data=json.dumps(self.data))
        response = self.app.delete("/api/v1/red-flags/1")
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(result['data']['message'], 'red-flag record has been deleted')

    def test_redflag_not_found(self):
        """Test a redflag not found"""
        response = self.app.get("/api/v1/red-flags/10")
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(result['error'], "Red-flag does not exist")

if __name__ == "__main__":
    unittest.main()
