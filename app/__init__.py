"""App module init file"""
from flask import Flask, Blueprint
from flask_cors import CORS
from instance.config import APP_CONFIG
from flask import jsonify, make_response
from app.db_config import create_tables, create_super_user

from app.api.v1.routes import VERSION_ONE as v1
from app.api.v2.routes import VERSION_TWO as v2

import uuid

def url_not_found(error):
    return make_response(jsonify({
        "status": 404,
        "error": "Page not found"
    }), 404)

def create_app(config_name='development'):
    """Method that creates the app and initializes configurations"""
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(APP_CONFIG[config_name])

    url = app.config.get('DATABASE_URL')
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    create_tables(url)

    public_id = str(uuid.uuid4())
    if config_name == 'testing':
        public_id = "f3b8a1c3-f775-49e1-991c-5bfb963eb419"
    create_super_user(url, public_id)

    app.register_error_handler(404, url_not_found)
    app.url_map.strict_slashes = False

    app.register_blueprint(v1)
    app.register_blueprint(v2)

    return app

