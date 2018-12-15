"""App module init file"""
from flask import Flask, Blueprint
from instance.config import APP_CONFIG
from flask import jsonify, make_response
from .db_config import create_tables, create_super_user
import os

from .api.v1.routes import VERSION_ONE as v1
from .api.v2.routes import VERSION_TWO as v2

def url_not_found(error):
    return make_response(jsonify({
        "status": 404,
        "error": "Page not found"
    }), 404)

def create_app(config_name='development'):
    """Method that creates the app and initializes configurations"""
    app = Flask(__name__, instance_relative_config=True)
    create_tables()
    create_super_user()
    app.register_error_handler(404, url_not_found)
    app.url_map.strict_slashes = False
    app.config.from_object(APP_CONFIG[config_name])

    app.register_blueprint(v1)
    app.register_blueprint(v2)

    return app

