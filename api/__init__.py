import os
from flask import Flask, jsonify, make_response, render_template, request
from flask_cors import CORS

from api.core import exception_handler, create_response
from api.db import Database


def create_app(**config):

    # Instantiate flask app
    app = Flask(__name__, instance_relative_config=True)

    # Add CORS headers
    CORS(app)

    # Register database
    Database(**config)
    Database.init_app(app)

    # proxy support for Nginx
    from werkzeug.middleware.proxy_fix import ProxyFix

    app.wsgi_app = ProxyFix(app.wsgi_app)

    # TODO: Add configurations from ENV
    # TODO: Add logger

    # Register blueprints for API endpoints
    from api.endpoints import main, filter_, patient_history_, patient_images_

    app.register_blueprint(main.main)
    app.register_blueprint(filter_.filter_)
    app.register_blueprint(patient_history_.patient_history_)
    app.register_blueprint(patient_images_.patient_images_)

    # Register error handler
    app.register_error_handler(Exception, exception_handler)

    return app
