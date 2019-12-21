import pytest
import api.db as db_utils
from api.db import Database


def test_get_close_db(app):
    with app.app_context():
        db_ = Database.get_db()
        assert db_ is Database.get_db()


def test_get_table_names(app):
    with app.app_context():
        res = db_utils.get_table_names()
    assert res is not None


def test_get_table_columns(app):
    with app.app_context():
        res = db_utils.get_table_columns("pt_deid")
    assert res is not None
