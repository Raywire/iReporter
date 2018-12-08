"""Incidents Models"""
import datetime
from flask import request
from flask_restful import reqparse
from app.db_config import connection, create_cursor
import re

url = "dbname='ireporter' host='localhost' port='5432' user='raywire' password='raywire2018'"
def validator(value):
    """method to check for only integers"""
    if not re.match(r"^[0-9]+$", value):
        raise ValueError("Pattern not matched")
def validate_coordinates(value):
    """method to check for valid coordinates"""
    if not re.match(r"^[-+]?([1-8]?\d(\.\d+)?|90(\.0+)?),\s*[-+]?(180(\.0+)?|((1[0-7]\d)|([1-9]?\d))(\.\d+)?)$", value):
        raise ValueError("Pattern not matched")
def validate_comment(value):
    """method to check comment only starts with A-Z"""
    if not re.match(r"[A-Za-z1-9]", value):
        raise ValueError("Pattern not matched")    

parser = reqparse.RequestParser(bundle_errors=True)
parser_location = reqparse.RequestParser(bundle_errors=True)
parser_status = reqparse.RequestParser(bundle_errors=True)

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

parser_status.add_argument('status',
                    choices=['draft', 'under investigation', 'rejected', 'resolved'],
                    required=True,
                    nullable=False,
                    help="This key is required and should not be empty or formatted wrongly(Accepted values: draft, under investigatin, rejected, resolved)"
                    )

class InterventionModel:
    """Intervention model class"""
    def __init__(self):
        self.db = connection(url)
        self.cursor = create_cursor(url)

    def save_intervention(self):
        """method to post one or multiple interventions"""
        args = parser.parse_args()
        data = {
            'createdOn' : datetime.datetime.utcnow(),
            'createdBy' : request.json.get('createdBy'),
            'type' : 'intervention',
            'location' : request.json.get('location'),
            'status' : "draft",
            'images' : request.json.get('images'),
            'videos' : request.json.get('videos'),
            'title' : request.json.get('title'),
            'comment' : request.json.get('comment')
        }

        query = """INSERT INTO incidents (createdon,createdby,type,location,status,images,videos,title,comment) VALUES('{0}',{1},'{2}','{3}','{4}','{5}','{6}','{7}','{8}');""".format(data['createdOn'],data['createdBy'],data['type'],data['location'],data['status'],data['images'],data['videos'],data['title'],data['comment'])
        conn = self.db
        cursor = conn.cursor()
        cursor.execute(query)
        conn.commit()
        return data

    def get_interventions(self):
        """method to get all interventions"""
        query = """SELECT * from incidents WHERE type='intervention'"""
        self.cursor.execute(query)
        interventions = self.cursor.fetchall()
        intervention_list = []

        for intervention in interventions:
            intervention_data = {
                'id' : intervention['id'],
                'createdOn' : intervention['createdon'],
                'createdBy' : intervention['createdby'],
                'type' : intervention['type'],
                'location' : intervention['location'],
                'status' : intervention['status'],
                'images' : intervention['images'],
                'videos' : intervention['videos'],
                'title' : intervention['title'],
                'comment' : intervention['comment']
            }            
            intervention_list.append(intervention_data)
        return intervention_list

    def get_intervention_by_id(self, intervention_id):
        "Method to get an intervention by id"
        query = """SELECT * from incidents WHERE type='intervention' AND id={0}""".format(intervention_id)
        self.cursor.execute(query)
        intervention = self.cursor.fetchone()

        if self.cursor.rowcount == 0:
            return None

        intervention_data = {
            'id' : intervention['id'],
            'createdOn' : intervention['createdon'],
            'createdBy' : intervention['createdby'],
            'type' : intervention['type'],
            'location' : intervention['location'],
            'status' : intervention['status'],
            'images' : intervention['images'],
            'videos' : intervention['videos'],
            'title' : intervention['title'],
            'comment' : intervention['comment']
        }
        return intervention_data

    def edit_intervention_status(self, intervention_id):
        "Method to edit an intervention's status"
        args = parser_status.parse_args()
        status = request.json.get('status')
        if self.get_intervention_by_id(intervention_id) == None:
            return None
        
        query = """UPDATE incidents SET status='{0}' WHERE id={1}""".format(status, intervention_id)
        conn = self.db
        cursor = conn.cursor()
        cursor.execute(query)
        conn.commit()
        return 'updated'

    def edit_intervention_location(self, intervention_id):
        "Method to edit an intervention's status"
        args = parser_location.parse_args()
        location = request.json.get('location')
        if self.get_intervention_by_id(intervention_id) == None:
            return None
        
        query = """UPDATE incidents SET location='{0}' WHERE id={1}""".format(location, intervention_id)
        conn = self.db
        cursor = conn.cursor()
        cursor.execute(query)
        conn.commit()
        return 'updated'  