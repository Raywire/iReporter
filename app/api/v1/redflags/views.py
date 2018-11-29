from flask_restful import Resource
from flask import jsonify, make_response, request, abort

import datetime

incidents = []


class RedFlags(Resource):
    """docstring for RedFlags"""
    
    def __init__(self):
        self.db = incidents
        if len(self.db) == 0:
            self.id = 1
        else:
            self.id = self.db[-1]['id'] + 1    

    def get(self):
        """method to get all redflags"""

        return make_response(jsonify({
            "status" : 200,
            "data" : self.db
        }), 200) 
       
    
    def post(self):
        """method to post a redflag"""
        
        data = {
            'id' : self.id,
            'createdOn' : datetime.datetime.utcnow(),
            'createdBy' : request.json['createdBy'],
            'type' : 'red-flags',
            'location' : request.json.get('location', ""),
            'status' : "draft",
            'images' : request.json.get('images', ""),
            'videos' : request.json.get('videos', ""),
            'title' : request.json['title'],
            'comment' : request.json.get('comment', "")
        }
        self.db.append(data)
        
        success_message = {
            "id" : self.id,
            "message" : "Created red-flag record"
        }

        return make_response(jsonify({
            "status" : 201,
            "data" : success_message
        }), 201)
    
class RedFlag(Resource):
    """docstring of RedFlag"""

    def __init__(self):
        self.db = incidents

    def get(self, redflag_id):
        """method to get a specific redflag"""

        for incident in self.db:
            if incident['id'] == redflag_id:
                return make_response(jsonify({
                    "status" : 200,
                    "data" : incident
                }), 200)
        return make_response(jsonify({
            "status" : 404,
            "error" : "Red-flag does not exist"
        }), 404)                
          
    def delete(self, redflag_id):
        """method to delete redflag"""
        for incident in self.db:
            if incident['id'] == redflag_id:
                self.db.remove(incident)

                success_message = {
                    "id" : redflag_id,
                    "message" : "red-flag record has been deleted"
                }

                return make_response(jsonify({
                    "status" : 200,
                    "data" : success_message
                }), 200)
        return make_response(jsonify({
            "status" : 404,
            "error" : "Red-flag does not exist"
        }), 404)

    def put(self, redflag_id):
        """method to update a redflag"""
        for incident in self.db:
            if incident['id'] == redflag_id:
                incident['createdBy'] = request.json.get('createdBy', incident['createdBy'])
                incident['location'] = request.json.get('location', incident['location'])
                incident['images'] = request.json.get('images', incident['images'])
                incident['videos'] = request.json.get('videos', incident['videos'])
                incident['title'] = request.json.get('title', incident['title'])
                incident['comment'] = request.json.get('comment', incident['comment'])

                success_message = {
                    "id" : redflag_id,
                    "message" : "Red-flag has been updated"
                }

                return make_response(jsonify({
                    "status" : 200,
                    "data" : success_message
                }), 200)
        return make_response(jsonify({
            "status" : 404,
            "error" : "Red-flag does not exist"
        }), 404)

