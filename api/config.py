"""
Configuration options for the api server.
TODO: Finish this file and documentation
"""

import os
from api.core import get_database_url


class Config:
    """Base config
    """

    SECRET_KEY = "somekey"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    LOG_FILE = "api.log"


class DevelopmentConfig(Config):
    """Development Configuration
    """

    DEBUG = True
    SQLALCHEMY_DATABASE_URI = get_database_url()


class ProductionConfig(Config):
    """Uses production database server."""

    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")


config_ = {"dev": DevelopmentConfig, "prod": ProductionConfig}
