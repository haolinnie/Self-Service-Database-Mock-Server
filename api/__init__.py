import os
from flask import Flask
from flask_cors import CORS
from werkzeug.middleware.proxy_fix import ProxyFix
from werkzeug.middleware.profiler import ProfilerMiddleware


from api.core import exception_handler
from api.config import _config
from api.models import db, models
from api.endpoints import _main, _filter, _patient_history, _patient_images, _users


def create_app(testing=False):
    """Flask Application Factory

    config_override isn't current used 
    """
    # Instantiate flask app
    app = Flask(__name__, instance_relative_config=True)

    # Set configurations
    env = os.environ.get("FLASK_ENV", "development")
    app.config.from_object(_config[env])
    if testing:
        app.config["TESTING"] = True

    # TODO: Add logger

    # Register database
    db.init_app(app)

    with app.app_context():
        db.create_all(bind=["users"])

        if env == "development":
            from api.models import User

            user = User(username="debug")
            user.hash_password("debug")
            db.session.add(user)
            user = User(username="SelfService2020@northwestern.edu")
            user.hash_password("SelfService2020")
            db.session.add(user)
            db.session.commit()

    # Add CORS headers
    CORS(app)

    # proxy support for Nginx
    app.wsgi_app = ProxyFix(app.wsgi_app)

    # Profile
    # app.wsgi_app = ProfilerMiddleware(app.wsgi_app)

    # Register blueprints for API endpoints
    app.register_blueprint(_main._main)
    app.register_blueprint(_filter._filter)
    app.register_blueprint(_patient_history._patient_history)
    app.register_blueprint(_patient_images._patient_images)
    app.register_blueprint(_users._users)

    # Register error handler
    app.register_error_handler(Exception, exception_handler)

    # Shell context
    @app.shell_context_processor
    def make_shell_context():
        return dict(db=db, models=models)

    return app
