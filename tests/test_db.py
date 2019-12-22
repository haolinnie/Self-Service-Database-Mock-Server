import pytest
from api.models import db, db_utils


def test_get_table_names(app):
    with app.app_context():
        res = db_utils.get_table_names()
    assert res is not None


def test_get_table_columns(app):
    with app.app_context():
        res = db_utils.get_table_columns("pt_deid")
    assert res is not None
