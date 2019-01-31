"""Views for incident uploads"""
from flask_restful import Resource
from flask import jsonify, send_from_directory, current_app
from app.api.v2.incidents.models import IncidentModel
from app.api.v2.decorator import (
    token_required, nonexistent_incident, owner_can_edit,
    draft_is_deletable, draft_is_editable)


class UploadInterventionImage(Resource):
    """Contains method for uploading an image to an intervention"""

    def __init__(self):
        self.intervention_upload_model = IncidentModel()

    @token_required
    def patch(current_user, self, intervention_id):
        """method to upload image to an intervention"""
        upload_status = self.intervention_upload_model.upload_incident_file(
            "intervention", intervention_id, current_user['id'], 'images')

        if upload_status is False:
            return jsonify({
                "status": 401,
                "message": "You cannot upload a photo for this incident"
            })

        if upload_status is None:
            return jsonify({
                "status": 404,
                "message": "Intervention does not exist"
            })

        if upload_status == 'No uploadFile name in form' or upload_status == 'File type not supported':
            return jsonify({
                "status": 400,
                "message": upload_status
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
            return jsonify({
                "status": 401,
                "message": "You cannot upload a video for this incident"
            })

        if upload_status == 'File type not supported' or upload_status == 'No uploadFile name in form':
            return jsonify({
                "status": 400,
                "message": upload_status
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
            return jsonify({
                "status": 401,
                "message": "You cannot upload a photo for this incident"
            })

        if upload_status == 'No uploadFile name in form' or upload_status == 'File type not supported':
            return jsonify({
                "status": 400,
                "message": upload_status
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

    def __init__(self):
        self.redflag_upload_model = IncidentModel()

    @token_required
    def patch(current_user, self, redflag_id):
        """method to upload videos to a redflag"""
        status = self.redflag_upload_model.upload_incident_file(
            "redflag", redflag_id, current_user['id'], 'videos')

        if status is None:
            return jsonify({
                "status": 404,
                "message": "Redflag does not exist"
            })

        if status == 'No uploadFile name in form' or status == 'File type not supported':
            return jsonify({
                "status": 400,
                "message": status
            })

        if status is False:
            return jsonify({
                "status": 401,
                "message": "You cannot upload a video for this incident"
            })

        if status is True:
            return jsonify({
                "status": 200,
                "data": [{
                    "id": redflag_id,
                    "message": "Video added to red-flag record",
                }]
            })


class Video(Resource):
    """"Contains method to get a video"""
    @token_required
    def get(current_user, self, filename):
        """Method to get a video"""
        video_url = IncidentModel().get_file_url('videos', filename)
        if video_url is None:
            return {
                "status": 404,
                "message": "Video does not exist"
            }, 404
        return video_url


class Image(Resource):
    """"Contains method to get an image"""

    @token_required
    def get(current_user, self, filename):
        """Method to get an image"""
        image_url = IncidentModel().get_file_url('images', filename)
        if image_url is None:
            return {
                "status": 404,
                "message": "Image does not exist"
            }, 404
        return image_url
