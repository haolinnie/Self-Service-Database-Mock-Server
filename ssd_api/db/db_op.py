import os
import sqlite3

from flask import g
from flask.cli import with_appcontext


db_path  = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    '../data/deid_data.db'
)

### Testing db functions

def test_con(): # pragma: no cover
    db = sqlite3.connect(db_path)
    return db

def test_execute(cmd): # pragma: no cover
    db = test_con()
    cursor = db.cursor()
    cursor.execute(cmd)
    res = cursor.fetchall()
    cursor.close()
    db.close()
    return res


### Flask server db functions

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(db_path)
    return g.db

def db_execute(cmd):
    db = get_db()
    cursor = db.cursor()
    cursor.execute(cmd)
    res = cursor.fetchall()
    cursor.close()
    return res

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_app(app):
    # Tell flask to cleanup
    app.teardown_appcontext(close_db)

