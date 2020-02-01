"""
Configuration options for the api server.
TODO: Finish this file and documentation
"""

import os
from api.core import get_database_url


class Config:
    """Base config
    """

    SECRET_KEY = b"\xca\xf1\xa41\xcf/\x98\x8a\xd7\x12\x92Z8=|\xe9"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    LOG_FILE = "api.log"


class DevelopmentConfig(Config):
    """Development Configuration
    Default, or set environmental variable `FLASK_ENV=development`
    """

    DEBUG = True
    credentials = get_database_url()
    SQLALCHEMY_DATABASE_URI = credentials["mssql_url_1"]
    SQLALCHEMY_BINDS = {
        "image_exams_db": credentials["mssql_url_2"],
        "users": credentials["users_db_url"],
    }


class ProductionConfig(Config):
    """Uses production database server.
    Set environmental variable `FLASK_ENV=production`
    Set secret key for cryptographically signing stuff
    """

    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get("MSSQL_CRED_1")
    SQLALCHEMY_BINDS = {"image_exams_db": os.environ.get("MSSQL_CRED_2")}
    # SECRET_KEY = os.environ.get("SECRET_KEY")


_config = {"development": DevelopmentConfig, "production": ProductionConfig}
