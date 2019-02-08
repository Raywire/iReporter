from functools import wraps
from app.api.v2.users.models import UserModel
from flask import jsonify, request, current_app

import jwt
import os
import datetime


def token_required(f):
    @wraps(f)
    def decorated(*args, ** kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return {
                "message": "Token is missing"
            }, 401
        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
            verification = data['verification']
            current_user = UserModel().get_user(data['public_id'])
            current_user.update({'verification': verification})
        except:
            return {
                "message": "Token is invalid"
            }, 401
        return f(current_user, *args, **kwargs)
    return decorated

def get_token(public_id, expiration, verification_status):
    token = jwt.encode({'public_id': public_id, 'verification': verification_status, 'exp': datetime.datetime.utcnow(
    ) + datetime.timedelta(minutes=expiration)}, current_app.config['SECRET_KEY'], algorithm='HS256')
    return token

def nonexistent_incident(incident_type):
    return jsonify({
        "status": 404,
        "message": "{0} does not exist".format(incident_type)
    })


def owner_can_edit():
    return jsonify({
        "status": 401,
        "message": "Only the user who created this record can edit it"
    })

def draft_is_editable():
    return jsonify({
        "status": 401,
        "message": "Incident can only be edited when the status is draft"
    })

def draft_is_deletable():
    return jsonify({
        "status": 401,
        "message": "Incident can only be deleted when the status is draft"
    })

def updated_incident(incident_id, incident_type, field):
    return jsonify({
        "status": 200,
        "data": [{
            "id": incident_id,
            "message": "Updated {0} record's {1}".format(incident_type, field)
        }]
    })