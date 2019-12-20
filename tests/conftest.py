import os
import tempfile

import pytest
from api import create_app


@pytest.fixture
def app():
    config = {'test': True}
    app = create_app(**config)
    yield app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()
