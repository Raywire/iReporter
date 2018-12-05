"""App module init file"""
from flask import Flask, Blueprint
from instance.config import APP_CONFIG

from .api.v1.routes import VERSION_ONE as v1

def create_app(config_name='development'):
    """Create app docstring"""
    app = Flask(__name__, instance_relative_config=True)
    app.url_map.strict_slashes = False
    app.config.from_object(APP_CONFIG[config_name])
    #app.config.from_pyfile('config.py')

    app.register_blueprint(v1)
    return app
