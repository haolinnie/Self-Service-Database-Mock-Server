"""
Configuration options for the api server.
TODO: Finish this file and documentation
"""

from base64 import b64encode
import os

from api.core import get_database_url


class Config:
    """Base config
    """

    DEBUG = False
    SECRET_KEY = b64encode(os.urandom(16)).decode()
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    LOG_FILE = "api.log"

    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(
        os.getcwd(), "data", "sample_db1.db"
    )
    SQLALCHEMY_BINDS = {
        "image_exams_db": "sqlite:///"
        + os.path.join(os.getcwd(), "data", "sample_db2.db"),
        "users": "sqlite:///",
    }


class DevelopmentConfig(Config):
    """Development Configuration
    Default, or set environmental variable `FLASK_ENV=development`
    """

    DEBUG = True


class ProductionConfig(Config):
    """Uses production database server.
    Set environmental variable `FLASK_ENV=production`
    """

    credentials = get_database_url()
    SQLALCHEMY_DATABASE_URI = credentials["mssql_url_1"]
    SQLALCHEMY_BINDS = {
        "image_exams_db": credentials["mssql_url_2"],
        "users": credentials["users_db"],
    }


class TestingConfig(Config):
    """Testing Config
    Set environmental variable `FLASK_ENV=testing`
    or
        app = create_app(testing=True)
    """

    DEBUG = True
    TESTING = True
