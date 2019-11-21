import os
import pymysql

from flask import g
from flask.cli import with_appcontext


db_path  = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    '../data/deid_data.db'
)

### Testing db functions

def test_con(): # pragma: no cover
    return pymysql.connect('localhost', 'test_user', 'password', 'ssd_sample_database')

def test_execute(cmd): # pragma: no cover
    db = test_con()
    cursor = db.cursor()
    cursor.execute(cmd)
    res = cursor.fetchall()
    cursor.close()
    db.close()
    return res


### Flask server db functions

class Database():
    test = False;
    host = 'localhost'
    username = 'test_user'
    password = 'password'
    db_name = 'ssd_sample_database'

    def __init__(self, **kwargs):
        if 'test' in kwargs:
            test = kwargs['test']
        if 'host' in kwargs:
            host = kwargs['host']
        if 'username' in kwargs:
            user = kwargs['username']
        if 'password' in kwargs:
            password = kwargs['password']
        if 'database' in kwargs:
            db_name in kwargs['database']

    @classmethod
    def get_db(cls):
        if 'db' not in g:
            g.db = pymysql.connect(cls.host, cls.username, cls.password, cls.db_name)
        return g.db

    @classmethod
    def db_execute(cls, cmd):
        with cls.get_db().cursor() as cursor:
            cursor.execute(cmd)
            res = cursor.fetchall()
        return res

    @staticmethod
    def close_db(e=None):
        db = g.pop('db', None)
        if db is not None:
            db.close()

    @classmethod
    def init_app(cls, app):
        # Tell flask to cleanup
        app.teardown_appcontext(cls.close_db)

    @classmethod
    def get_table_names(cls):
        with cls.get_db().cursor() as cursor:
            cursor.execute('''SELECT table_name FROM information_schema.tables
            WHERE table_schema = %s;''', cls.db_name)
            table_names = cursor.fetchall()
        return [v[0] for v in table_names]

    @classmethod
    def get_table_columns(cls, table_name):
        with cls.get_db().cursor() as cursor:
            cursor.execute('''SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS
            WHERE table_name = %s;''', table_name)
            col_names = cursor.fetchall()
        return [v[0] for v in col_names]
