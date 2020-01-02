"""
Configuration options for the api server.
TODO: Finish this file and documentation
"""

import os
from .core import get_database_url


class Config:
    """Base config
    """

    SECRET_KEY = "somekey"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    LOG_FILE = "api.log"


class DevelopmentConfig(Config):
    """Development Configuration
    Default, or set environmental variable `FLASK_ENV=development`
    """

    DEBUG = True
    SQLALCHEMY_DATABASE_URI = get_database_url()


class ProductionConfig(Config):
    """Uses production database server.
    Set environmental variable `FLASK_ENV=production`
    """

    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")


_config = {"development": DevelopmentConfig, "production": ProductionConfig}
