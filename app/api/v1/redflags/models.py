"""Redflag Models"""
import datetime
from flask import request
from flask_restful import reqparse
from app.validators import validate_coordinates, validate_comment, validator

INCIDENTS = []

parser = reqparse.RequestParser(bundle_errors=True)
parser_location = reqparse.RequestParser(bundle_errors=True)

parser.add_argument('createdBy',
                    type=validator,
                    required=True,
                    nullable=False,
                    help="This key is required and should not be empty or formatted wrongly"
                    )

parser.add_argument('location',
                    type=validate_coordinates,
                    required=True,
                    nullable=False,
                    help="This key is required and should not be empty or formatted wrongly"
                    )

parser_location.add_argument('location',
                    type=validate_coordinates,
                    required=True,
                    nullable=False,
                    help="This key is required and should not be empty or formatted wrongly"
                    )

parser.add_argument('comment',
                    type=validate_comment,
                    required=True,
                    nullable=False,
                    help="This key is required and should not be empty or formatted wrongly"
                    )
parser.add_argument('title',
                    type=validate_comment,
                    required=True,
                    nullable=False,
                    help="This key is required and should not be empty or formatted wrongly"
                    )
class RedFlagModel:
    """Redflag model class"""
    def __init__(self):
        self.db = INCIDENTS
        if not self.db:
            self.id = 1
        else:
            self.id = self.db[-1]['id'] + 1

    def get_redflags(self):
        """method to get all red-flags"""
        if not self.db:
            return None
        return self.db

    def save_redflag(self):
        """method to post all red-flags"""
        args = parser.parse_args()
        data = {
            'id' : self.id,
            'createdOn' : datetime.datetime.utcnow(),
            'createdBy' : request.json.get('createdBy'),
            'type' : 'red-flags',
            'location' : request.json.get('location'),
            'status' : "draft",
            'images' : request.json.get('images'),
            'videos' : request.json.get('videos'),
            'title' : request.json.get('title'),
            'comment' : request.json.get('comment')
        }

        self.db.append(data)
        return data


    def get_redflag(self, redflag_id):
        "Method to get a redflag"
        for incident in self.db:
            if incident['id'] == redflag_id:
                return incident
        return None

    def delete_redflag(self, incident):
        "Method to delete a redflag"
        self.db.remove(incident)
        return True

    def edit_redflag_location(self, incident):
        "Method to edit a redflag's location"
        parser_location.parse_args()
        incident['location'] = request.json.get('location')
        return "updated"

    def edit_redflag_comment(self, incident):
        "Method to edit a redflag's comment"
        incident['comment'] = request.json.get('comment', 'keyerror')
        if incident['comment'] == 'keyerror' or incident['comment'] == '':
            return "keyerror"
        return "updated"

    def edit_redflag(self, incident):
        """Method to edit redflag fields"""
        args = parser.parse_args()
        incident['createdBy'] = request.json.get('createdBy')
        incident['location'] = request.json.get('location')
        incident['status'] = request.json.get('status')
        incident['images'] = request.json.get('images')
        incident['videos'] = request.json.get('videos')
        incident['title'] = request.json.get('title')
        incident['comment'] = request.json.get('comment')

        return "updated"
        