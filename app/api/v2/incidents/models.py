"""Incidents Models"""
import datetime
from flask import request, session
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
parser_comment = reqparse.RequestParser(bundle_errors=True)

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

parser_comment.add_argument('comment',
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

class IncidentModel:
    """Class with methods to perform Create, Read, Update and Delete operations on database"""
    def __init__(self):
        self.db = connection(url)
        self.cursor = create_cursor(url)

    def save_incident(self,incident_type):
        """method to post one or multiple incidents"""
        args = parser.parse_args()
        data = {
            'createdOn' : datetime.datetime.utcnow(),
            'createdBy' : session['id'],
            'type' : incident_type,
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

    def get_incidents(self, incident_type):
        """method to get all incidents"""
        query = """SELECT * from incidents WHERE type='{0}'""".format(incident_type)
        self.cursor.execute(query)
        incidents = self.cursor.fetchall()
        incident_list = []

        if self.cursor.rowcount == 0:
            return None        

        for incident in incidents:
            incident_data = {
                'id' : incident['id'],
                'createdOn' : incident['createdon'],
                'createdBy' : incident['createdby'],
                'type' : incident['type'],
                'location' : incident['location'],
                'status' : incident['status'],
                'images' : incident['images'],
                'videos' : incident['videos'],
                'title' : incident['title'],
                'comment' : incident['comment']
            }            
            incident_list.append(incident_data)
        return incident_list

    def get_incident_by_id(self, incident_type,intervention_id):
        "Method to get an incident by id"
        query = """SELECT * from incidents WHERE type='{0}' AND id={1}""".format(incident_type, intervention_id)
        self.cursor.execute(query)
        incident = self.cursor.fetchone()

        if self.cursor.rowcount == 0:
            return None

        incident_data = {
            'id' : incident['id'],
            'createdOn' : incident['createdon'],
            'createdBy' : incident['createdby'],
            'type' : incident['type'],
            'location' : incident['location'],
            'status' : incident['status'],
            'images' : incident['images'],
            'videos' : incident['videos'],
            'title' : incident['title'],
            'comment' : incident['comment']
        }
        return incident_data

    def edit_incident_status(self, incident_type, incident_id):
        "Method to edit an incident's status"
        args = parser_status.parse_args()
        status = request.json.get('status')
        if self.get_incident_by_id(incident_type, incident_id) == None:
            return None
        
        query = """UPDATE incidents SET status='{0}' WHERE id={1}""".format(status, incident_id)
        conn = self.db
        cursor = conn.cursor()
        cursor.execute(query)
        conn.commit()
        return 'updated'

    def edit_incident_location(self, incident_type, incident_id):
        "Method to edit an incident's location"
        args = parser_location.parse_args()
        location = request.json.get('location')
        incident = self.get_incident_by_id(incident_type, incident_id)
        if incident == None:
            return None
        if session['id'] != incident['createdBy']:
            return 'no access'
        
        query = """UPDATE incidents SET location='{0}' WHERE id={1}""".format(location, incident_id)
        conn = self.db
        cursor = conn.cursor()
        cursor.execute(query)
        conn.commit()
        return 'updated'  

    def edit_incident_comment(self, incident_type, incident_id):
        "Method to edit an incident's comment"
        args = parser_comment.parse_args()
        comment = request.json.get('comment')
        incident = self.get_incident_by_id(incident_type, incident_id)
        if incident == None:
            return None

        if session['id'] != incident['createdBy']:
            return 'no access'            
        
        query = """UPDATE incidents SET comment='{0}' WHERE id={1}""".format(comment, incident_id)
        conn = self.db
        cursor = conn.cursor()
        cursor.execute(query)
        conn.commit()
        return 'updated'

    def delete_incident(self, incident_type, incident_id):
        "Method to delete an incident record"
        incident = self.get_incident_by_id(incident_type, incident_id)
        if incident == None:
            return None

        if session['id'] != incident['createdBy']:
            return 'no access'  

        query = """DELETE FROM incidents WHERE id={0}""".format(incident_id)
        conn = self.db
        cursor = conn.cursor()
        cursor.execute(query)
        conn.commit()
        return 'deleted'