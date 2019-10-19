import os
import tempfile

import pytest
from ssd_api import create_app
from ssd_api.db_op import get_db


@pytest.fixture
def app():

    app = create_app({
        'TESTING': True,
    })

    yield app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()
