import os
import tempfile

import pytest
from api import create_app
from api.models import db
from api.models.User import User


@pytest.fixture
def app():
    app = create_app(testing=True)
    yield app


@pytest.fixture
def app_notest():
    app = create_app(testing=False)
    yield app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def auth_token(app_notest):
    with app_notest.app_context():
        user = User(username="username")
        user.hash_password("password")
        db.session.add(user)
        db.session.commit()
        token = user.generate_auth_token()
    yield token


@pytest.fixture
def runner(app):
    return app.test_cli_runner()
