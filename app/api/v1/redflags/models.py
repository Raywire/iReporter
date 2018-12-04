"""Redflag Models"""
import datetime
from flask import request

INCIDENTS = []

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
        return self.db

    def save_redflag(self):
        """method to post all red-flags"""
        data = {
            'id' : self.id,
            'createdOn' : datetime.datetime.utcnow(),
            'createdBy' : request.json.get('createdBy', 'keyerror'),
            'type' : 'red-flags',
            'location' : request.json.get('location', ''),
            'status' : "draft",
            'images' : request.json.get('images', ''),
            'videos' : request.json.get('videos', ''),
            'title' : request.json.get('title', ''),
            'comment' : request.json.get('comment', '')
        }
        if data['createdBy'] == "keyerror":
            return "keyerror"
        self.db.append(data)
        return self.id

    def get_redflag(self, redflag_id):
        "Method to get a redflag"
        for incident in self.db:
            if incident['id'] == redflag_id:
                return incident
        return "no redflag"

    def delete_redflag(self, incident):
        "Method to delete a redflag"
        self.db.remove(incident)
        return "deleted"

    def edit_redflag_location(self, incident):
        "Method to edit a redflag's location"
        incident['location'] = request.json.get('location', 'keyerror')
        if incident['location'] == 'keyerror':
            return "keyerror"
        return "updated"

    def edit_redflag_comment(self, incident):
        "Method to edit a redflag's comment"
        incident['comment'] = request.json.get('comment', 'keyerror')
        if incident['comment'] == 'keyerror':
            return "keyerror"
        return "updated"

    def edit_redflag(self, incident):
        """Method to edit redflag fields"""
        incident['createdBy'] = request.json.get('createdBy', incident['createdBy'])
        incident['location'] = request.json.get('location', incident['location'])
        incident['status'] = request.json.get('status', incident['status'])
        incident['images'] = request.json.get('images', incident['images'])
        incident['videos'] = request.json.get('videos', incident['videos'])
        incident['title'] = request.json.get('title', incident['title'])
        incident['comment'] = request.json.get('comment', incident['comment'])

        return "updated"
        