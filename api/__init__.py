import os
from flask import Flask
from flask_cors import CORS
from werkzeug.middleware.proxy_fix import ProxyFix

from api.core import exception_handler, create_response
from api.config import _config
from api.models import db, models
from api.endpoints import _main, _filter, _patient_history, _patient_images


def create_app(**config_override):
    """Flask Application Factory

    config_override isn't current used 
    """
    # Instantiate flask app
    app = Flask(__name__, instance_relative_config=True)

    # Set configurations
    env = os.environ.get("FLASK_ENV", "development")
    app.config.from_object(_config[env])

    # Register database
    db.init_app(app)

    # Add CORS headers
    CORS(app)

    # TODO: Add logger

    # proxy support for Nginx
    app.wsgi_app = ProxyFix(app.wsgi_app)

    # Register blueprints for API endpoints
    app.register_blueprint(_main._main)
    app.register_blueprint(_filter._filter)
    app.register_blueprint(_patient_history._patient_history)
    app.register_blueprint(_patient_images._patient_images)

    # Register error handler
    app.register_error_handler(Exception, exception_handler)

    # Shell context
    @app.shell_context_processor
    def make_shell_context():
        return dict(db=db, models=models)

    return app
