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
       
