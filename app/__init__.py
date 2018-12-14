"""App module init file"""
from flask import Flask, Blueprint
from instance.config import APP_CONFIG
from flask import jsonify, make_response
from app.db_config import create_tables, create_super_user
from flask_mail import Mail, Message
import os

from .api.v1.routes import VERSION_ONE as v1
from .api.v2.routes import VERSION_TWO as v2

email_address = os.getenv('MAIL_USERNAME')
email_password = os.getenv('MAIL_PASSWORD')

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

    mail = Mail(app)
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USERNAME'] = email_address
    app.config['MAIL_PASSWORD'] = email_password
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_USE_SSL'] = True

    return app

def send_message(intervention_id,status,intervention_type,email):
    app = create_app()
    mail = Mail(app)
    msg = Message("Incident Status Change", sender='ireporterandela@gmail.com', recipients=[email])
    msg.body = "The status of your {0} with id: {1} has been changed to {2}".format(intervention_type, intervention_id, status)
    with app.app_context():
       mail.send(msg)    

    return "Sent"
