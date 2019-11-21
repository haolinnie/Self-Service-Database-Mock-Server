import pytest
from ssd_api.db import Database as db


def test_get_close_db(app):
    with app.app_context():
        db_ = db.get_db()
        assert db_ is db.get_db()


def test_get_table_names(app):
    with app.app_context():
        res = db.get_table_names()
    assert res is not None


def test_get_table_columns(app):
    with app.app_context():
        res = db.get_table_columns('pt_deid')
    assert res is not None