import sqlite3

import pytest
from ssd_api import db


def test_get_close_db(app):
    with app.app_context():
        db_ = db.get_db()
        assert db_ is db.get_db()

    with pytest.raises(sqlite3.ProgrammingError) as e:
        db_.execute('SELECT 1')

    assert 'closed' in str(e.value)

def test_get_table_names(app):
    with app.app_context():
        res = db.get_table_names()
    assert res is not None

def test_get_table_columns(app):
    with app.app_context():
        res = db.get_table_columns('pt_deid')
    assert res is not None