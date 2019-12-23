import os
from flask import Flask, jsonify, make_response, render_template, request
from flask_cors import CORS

from api.core import exception_handler, create_response
from api.config import config_
from api.models import db


def create_app(**config_override):
    """Flask Application Factory
    """
    # Instantiate flask app
    app = Flask(__name__, instance_relative_config=True)

    # Set configurations
    env = os.environ.get("FLASK_ENV", "development")
    print(env)
    app.config.from_object(config_[env])

    db.init_app(app)  # Register database
    CORS(app)  # Add CORS headers

    # TODO: Add logger

    # proxy support for Nginx
    from werkzeug.middleware.proxy_fix import ProxyFix

    app.wsgi_app = ProxyFix(app.wsgi_app)

    # Register blueprints for API endpoints
    from api.endpoints import main, filter_, patient_history_, patient_images_

    app.register_blueprint(main.main)
    app.register_blueprint(filter_.filter_)
    app.register_blueprint(patient_history_.patient_history_)
    app.register_blueprint(patient_images_.patient_images_)

    # Register error handler
    app.register_error_handler(Exception, exception_handler)

    return app
