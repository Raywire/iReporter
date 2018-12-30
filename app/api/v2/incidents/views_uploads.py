"""Views for incident uploads"""
from flask_restful import Resource
from flask import jsonify, send_from_directory
from app.api.v2.incidents.models import IncidentModel
from app.api.v2.send_email import send
from app.api.v2.decorator import (
    token_required, nonexistent_incident, owner_can_edit, draft_is_deletable, draft_is_editable, updated_incident)

import os

UPLOAD_FOLDER_IMAGE = 'upload/images'
UPLOAD_FOLDER_VIDEO = 'upload/videos'
APP_ROOT = os.path.dirname(os.path.abspath(__file__))

class UploadInterventionImage(Resource):
    """Contains method for uploading an image to an intervention"""

    @token_required
    def patch(current_user, self, intervention_id):
        """method to upload image to an intervention"""
        upload_status = IncidentModel().upload_incident_file(
            "intervention", intervention_id, current_user['id'], 'images')

        if upload_status is None:
            return jsonify({
                "status": 404,
                "message": "Intervention does not exist"
            })

        if upload_status is False:
            return owner_can_edit()

        if upload_status == 'not draft':
            return draft_is_editable()            

        if upload_status == 'No uploadFile name' or upload_status == 'No file selected':
            return jsonify({
                "status" : 400,
                "message": "No uploadFile name in form or no file selected"
            })
        if upload_status == 'File type not supported':
            return jsonify({
                "status" : 400,
                "message": "File type not supported"
            })    

        if upload_status is True:
            return jsonify({
                "status": 200,
                "data": [{
                    "id": intervention_id,
                    "message": "Image added to intervention record",
                }]
            })

class UploadInterventionVideo(Resource):
    """Contains method for uploading an videos to an intervention"""

    @token_required
    def patch(current_user, self, intervention_id):
        """method to upload videos to an intervention"""
        upload_status = IncidentModel().upload_incident_file(
            "intervention", intervention_id, current_user['id'], 'videos')

        if upload_status is None:
            return jsonify({
                "status": 404,
                "message": "Intervention does not exist"
            })

        if upload_status is False:
            return owner_can_edit()

        if upload_status == 'not draft':
            return draft_is_editable() 

        if upload_status == 'No uploadFile name' or upload_status == 'No file selected':
            return jsonify({
                "status" : 400,
                "message": "No uploadFile name in form or no file selected"
            })
        if upload_status == 'File type not supported':
            return jsonify({
                "status" : 400,
                "message": "File type not supported"
            })    

        if upload_status is True:
            return jsonify({
                "status": 200,
                "data": [{
                    "id": intervention_id,
                    "message": "Video added to intervention record",
                }]
            })

class UploadRedflagImage(Resource):
    """Contains method for uploading an image to a red flag"""

    @token_required
    def patch(current_user, self, redflag_id):
        """method to upload image to red flag"""
        upload_status = IncidentModel().upload_incident_file(
            "redflag", redflag_id, current_user['id'], 'images')

        if upload_status is None:
            return nonexistent_incident("Redflag")

        if upload_status is False:
            return owner_can_edit()

        if upload_status == 'not draft':
            return draft_is_editable() 

        if upload_status == 'No uploadFile name' or upload_status == 'No file selected':
            return jsonify({
                "status" : 400,
                "message": "No uploadFile name in form or no file selected"
            })
        if upload_status == 'File type not supported':
            return jsonify({
                "status" : 400,
                "message": "File type not supported"
            })    

        if upload_status is True:
            return jsonify({
                "status": 200,
                "data": [{
                    "id": redflag_id,
                    "message": "Image added to red-flag record",
                }]
            })

class UploadRedflagVideo(Resource):
    """Contains method for uploading an videos to a red flags"""

    @token_required
    def patch(current_user, self, redflag_id):
        """method to upload videos to a redflag"""
        upload_status = IncidentModel().upload_incident_file(
            "redflag", redflag_id, current_user['id'], 'videos')

        if upload_status is None:
            return jsonify({
                "status": 404,
                "message": "Redflag does not exist"
            })

        if upload_status is False:
            return owner_can_edit()

        if upload_status == 'not draft':
            return draft_is_editable() 

        if upload_status == 'No uploadFile name' or upload_status == 'No file selected':
            return jsonify({
                "status" : 400,
                "message": "No uploadFile name in form or no file selected"
            })
        if upload_status == 'File type not supported':
            return jsonify({
                "status" : 400,
                "message": "File type not supported"
            })    

        if upload_status is True:
            return jsonify({
                "status": 200,
                "data": [{
                    "id": redflag_id,
                    "message": "Video added to red-flag record",
                }]
            })

class Video(Resource):
    @token_required
    def get(current_user, self, filename):
        try:
            target = os.path.join(APP_ROOT, UPLOAD_FOLDER_VIDEO)
            return send_from_directory(target, filename)
        except:
            return jsonify({
                "status": 404,
                "message": "Video does not exist"
            })

class Image(Resource):
    @token_required
    def get(current_user, self, filename):
        try:
            target = os.path.join(APP_ROOT, UPLOAD_FOLDER_IMAGE)
            return send_from_directory(target, filename)
        except:
            return jsonify({
                "status": 404,
                "message": "Image does not exist"
            })
