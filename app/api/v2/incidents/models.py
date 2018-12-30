"""Incidents Models"""
import datetime
from flask import request
from flask_restful import reqparse
from app.db_config import connection, init_database
from app.validators import validate_comment, validate_coordinates, validator
from werkzeug.utils import secure_filename
import psycopg2.extras
import os


UPLOAD_FOLDER_IMAGE = 'upload/images'
UPLOAD_FOLDER_VIDEO = 'upload/videos'
ALLOWED_EXTENSIONS_IMAGE = set(['png', 'jpg', 'jpeg', 'gif'])
ALLOWED_EXTENSIONS_VIDEO = set(['mp4', 'avi', 'flv', 'wmv', 'mov'])

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

parser.add_argument('comment',
                    type=validate_comment,
                    required=True,
                    trim=True,
                    nullable=False,
                    help="This key is required and should not be empty or formatted wrongly"
                    )

parser.add_argument('title',
                    type=validate_comment,
                    required=True,
                    trim=True,
                    nullable=False,
                    help="This key is required and should not be empty or formatted wrongly"
                    )


class IncidentModel:
    """Class with methods to perform Create, Read, Update, 
        Upload and Delete operations on database"""

    def __init__(self):
        self.db = init_database()

    def execute_query(self, query):
        conn = self.db
        cursor = conn.cursor()
        cursor.execute(query)
        conn.commit()
        cursor.close()
        conn.close()

    def allowed_file(self, filename, filetype):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in filetype

    def save_incident(self, incident_type, user_id):
        """method to post one or multiple incidents"""
        args = parser.parse_args()
        data = {
            'createdOn': datetime.datetime.utcnow(),
            'createdBy': user_id,
            'type': incident_type,
            'location': request.json.get('location'),
            'status': "draft",
            'images': request.json.get('images'),
            'videos': request.json.get('videos'),
            'title': request.json.get('title'),
            'comment': request.json.get('comment')
        }

        query = """INSERT INTO incidents (createdon,createdby,type,location,status,images,videos,title,comment) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
        values = data['createdOn'], data['createdBy'], data['type'], data['location'], data[
            'status'], data['images'], data['videos'], data['title'], data['comment']

        conn = self.db
        cursor = conn.cursor()
        cursor.execute(query, values)
        conn.commit()
        return data

    def get_incidents(self, incident_type):
        """method to get all incidents"""
        query = """SELECT incidents.comment,incidents.createdby,\
            incidents.createdon, incidents.id,incidents.images,\
            incidents.location,incidents.status,incidents.videos,\
            incidents.title,incidents.type, users.username from incidents \
            INNER JOIN users ON incidents.createdby=users.id WHERE type='{0}'\
            ORDER BY createdon DESC""".format(
            incident_type)
        conn = self.db
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cursor.execute(query)
        incidents = cursor.fetchall()
        incident_list = []

        if cursor.rowcount == 0:
            return None

        for incident in incidents:
            incident_list.append(incident)
        return incident_list

    def get_incident_by_id(self, incident_type, incident_id):
        """Method to get an incident by id"""
        query = """SELECT incidents.comment,incidents.createdby,\
        incidents.createdon, incidents.id,incidents.images,\
        incidents.location,incidents.status,incidents.videos,\
        incidents.title,incidents.type, users.username from incidents\
        INNER JOIN users ON incidents.createdby=users.id\
        WHERE type='{0}' AND incidents.id={1}""".format(
            incident_type, incident_id)
        conn = self.db
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cursor.execute(query)
        incident = cursor.fetchone()

        if cursor.rowcount == 0:
            return None

        return incident

    def edit_incident_status(self, incident_type, incident_id):
        """Method to edit an incident's status"""
        parser_status.add_argument('status',
                                   choices=['draft', 'under investigation',
                                            'rejected', 'resolved'],
                                   required=True,
                                   nullable=False,
                                   help="(Accepted values: draft, under investigation, rejected, resolved)"
                                   )
        args = parser_status.parse_args()
        status = request.json.get('status')
        if self.get_incident_by_id(incident_type, incident_id) is None:
            return None

        query = """UPDATE incidents SET status='{0}' WHERE id={1}""".format(
            status, incident_id)
        self.execute_query(query)
        return True

    def get_incident_status(self):
        current_status = request.json.get('status')
        return current_status

    def edit_incident_location(self, incident_type, incident_id, current_user_id):
        """Method to edit an incident's location"""
        parser_location.add_argument('location',
                                     type=validate_coordinates,
                                     required=True,
                                     nullable=False,
                                     help="This key is required and should not be empty or formatted wrongly"
                                     )
        args = parser_location.parse_args()
        location = request.json.get('location')
        incident = self.get_incident_by_id(incident_type, incident_id)
        if incident is None:
            return None
        if current_user_id != incident['createdby']:
            return False
        if incident['status'] != 'draft':
            return 'not draft'

        query = """UPDATE incidents SET location='{0}' WHERE id={1}""".format(
            location, incident_id)
        self.execute_query(query)
        return True

    def edit_incident_comment(self, incident_type, incident_id, current_user_id):
        """Method to edit an incident's comment"""
        parser_comment.add_argument('comment',
                                    type=validate_comment,
                                    required=True,
                                    nullable=False,
                                    help="This key is required and should not be empty or formatted wrongly"
                                    )
        args = parser_comment.parse_args()
        comment = request.json.get('comment')
        incident = self.get_incident_by_id(incident_type, incident_id)
        if incident is None:
            return None

        if current_user_id != incident['createdby']:
            return False

        if incident['status'] != 'draft':
            return 'not draft'

        query = """UPDATE incidents SET comment=%s WHERE id=%s"""
        values = comment, incident_id
        conn = self.db
        cursor = conn.cursor()
        cursor.execute(query, values)
        conn.commit()
        return True

    def delete_incident(self, incident_type, incident_id, current_user_id):
        """Method to delete an incident record"""
        incident = self.get_incident_by_id(incident_type, incident_id)
        if incident is None:
            return None

        if current_user_id != incident['createdby']:
            return False

        if incident['status'] != 'draft':
            return 'not draft'

        query = """DELETE FROM incidents WHERE id={0}""".format(incident_id)
        self.execute_query(query)
        return True

    def upload_incident_file(self, incident_type, incident_id, current_user_id, file_type):
        """Method to upload files to folder and insert file name into database"""

        incident = self.get_incident_by_id(incident_type, incident_id)
        if incident is None:
            return None

        if current_user_id != incident['createdby']:
            return False

        if incident['status'] != 'draft':
            return 'not draft'

        if 'uploadFile' not in request.files:
            return "No uploadFile name in form"

        uploads = request.files.getlist('uploadFile')

        for upload in uploads:

            if file_type == 'videos':
                allowed_file_type = ALLOWED_EXTENSIONS_VIDEO
                upload_file_folder = UPLOAD_FOLDER_VIDEO
                query = """UPDATE incidents SET videos=%s WHERE id=%s"""

            if file_type == 'images':
                allowed_file_type = ALLOWED_EXTENSIONS_IMAGE
                upload_file_folder = UPLOAD_FOLDER_IMAGE
                query = """UPDATE incidents SET images=%s WHERE id=%s"""

            if upload and self.allowed_file(upload.filename, allowed_file_type):
                filename = secure_filename(upload.filename)
                extension = filename.rsplit('.', 1)[1].lower()
                filename = datetime.datetime.utcnow().strftime('%s') + '.' + extension

                APP_ROOT = os.path.dirname(os.path.abspath(__file__))
                target = os.path.join(APP_ROOT, upload_file_folder, filename)
                upload.save(target)

                values = filename, incident_id
                conn = self.db
                cursor = conn.cursor()
                cursor.execute(query, values)
                conn.commit()
                return True

            return "File type not supported"
