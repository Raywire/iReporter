from functools import wraps
from app.api.v2.users.models import UserModel
from flask import jsonify, request

import jwt
import datetime
import os

secret_key = os.getenv('SECRET_KEY')


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
            data = jwt.decode(token, secret_key, algorithms=['HS256'])
            current_user = UserModel().get_user_by_public_id(data['public_id'])
        except:
            return {
                "message": "Token is invalid"
            }, 401
        return f(current_user, *args, **kwargs)
    return decorated
