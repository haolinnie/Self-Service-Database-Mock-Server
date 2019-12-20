'''
Database wrapper class for the pymysql connector to a MySQL Database
aimed at providing thread-safe connection for Flask
'''
import pymysql
from flask import g
from flask.cli import with_appcontext


### Flask server db functions

### TODO: Make the database fail gracefully when it fails to connect

class Database():
    test = False;
    host = 'localhost'
    username = 'test_user'
    password = 'password'
    db_name = 'ssd_sample_database'

    def __init__(self, **kwargs):
        '''
        Set up initialiser to populate database credentials
        This is probably not secure
        '''
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
        '''Make sure there's only one db connection open'''
        if 'db' not in g:
            g.db = pymysql.connect(cls.host, cls.username, cls.password, cls.db_name)
        return g.db


    @classmethod
    def init_app(cls, app):
        '''Tell flask to cleanup'''
        app.teardown_appcontext(cls.close_db)

    @staticmethod
    def close_db(e=None):
        '''Clean up'''
        db = g.pop('db', None)
        if db is not None:
            db.close()
