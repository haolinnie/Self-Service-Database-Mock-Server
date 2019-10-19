import sqlite3

import pytest
from ssd_api.db_op import get_db, get_table_names


def test_get_close_db(app):
    with app.app_context():
        db = get_db()
        assert db is get_db()

    with pytest.raises(sqlite3.ProgrammingError) as e:
        db.execute('SELECT 1')

    assert 'closed' in str(e.value)

def test_get_table_names(app):
    with app.app_context():
        res = get_table_names()
    
    assert res is not None