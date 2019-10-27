#!../flask/bin/python
import os
import sys
from flask import Flask, jsonify
from flask import make_response
from flask_restful import Resource, Api, reqparse

from ssd_api.util import get_documentation
from ssd_api.db_op import (
    get_db, get_table_names, sqlite3,
    init_app, db_execute
)
from ssd_api.config import Config

config = Config(os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    'setting.config'
))


# Initialise request parser
parser = reqparse.RequestParser()
parser.add_argument('table_name', type=str, help='ERROR: empty table name')
parser.add_argument('col_name', type=str, help='ERROR: empty column name')
parser.add_argument('pt_id', type=int, action='append', help='ERROR: empty pt_id_list')


class TableNames(Resource):
    def get(self):
        return {'table_names': get_table_names()}


class GetTable(Resource):
    def get(self, table_name):
        # Get table from db
        try:
            with get_db() as connection:
                cursor = connection.cursor()
                cursor.execute("SELECT * FROM {}".format(table_name))
                names = list(map(lambda x: x[0], cursor.description))
                data = cursor.fetchall()
                cursor.close()
        except sqlite3.OperationalError:
            return {"ERROR": "table doesn't exist."}

        return {'columns': names, 'data': data}


class GetTableCols(Resource):
    def get(self):
        data = parser.parse_args()
        table_name = data.get('table_name')

        # error handling
        if table_name is None:
            return {'ERROR': 'empty table_name'}

        # Get table columns
        try:
            with get_db() as connection:
                cursor = connection.cursor()
                cursor.execute("SELECT * FROM {}".format(table_name))
                names = list(map(lambda x: x[0], cursor.description))
                cursor.close()
        except sqlite3.OperationalError:
            return {"ERROR": "table doesn't exist."}

        return {'table_name': table_name, 'columns': names}


class GetDistinctX(Resource):
    def get(self):
        # print("[DEBUG] Get Distinct Called")
        data = parser.parse_args()
        col_name = data.get('col_name')
        table_name = data.get('table_name')

        # error handling
        if table_name is None:
            return {'ERROR': 'empty table_name'}
        if col_name is None:
            return {'ERROR': 'empty col_name'}

        try:
            cmd = "SELECT DISTINCT {} FROM {}".format(col_name, table_name)
            data = db_execute(cmd)
            data = [r[0] for r in data]
        except sqlite3.OperationalError:
            return {"ERROR": "sqlite3.OperationalError"}
        
        return {"data": data, "table_name": table_name, "col_name": col_name}


class FilterTableWithPTID(Resource):
    def get(self):
        data = parser.parse_args()
        pt_id = data.get('pt_id')
        table_name = data.get('table_name')

        if not pt_id:
            return {'ERROR': 'Must provide at least 1 pt_id'}
        if not table_name:
            return {'ERROR': 'Must provide table_name'}

        ### Select values from tables with given pt_id
        pt_id = "'" + "', '".join([str(v) for v in pt_id]) + "'"
        # print(pt_id)

        out_cols = "*"
        cmd = """
        SELECT {}
        FROM {}
        WHERE pt_id IN({})
        ORDER BY pt_id
        """.format(out_cols, table_name, pt_id)

        # Filter table for pt_id
        try:
            with get_db() as connection:
                cursor = connection.cursor()
                cursor.execute(cmd)
                col_names = list(map(lambda x: x[0], cursor.description))
                res = cursor.fetchall()
                cursor.close()
        except sqlite3.OperationalError:
            return {"ERROR": "Query error."}

        return {'columns': col_names, 'data': res}


def create_app(test_config=None):

    # Instantiate flask app
    app = Flask(__name__, instance_relative_config=True)
    init_app(app)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # proxy support for Nginx
    from werkzeug.middleware.proxy_fix import ProxyFix
    app.wsgi_app = ProxyFix(app.wsgi_app)

    # Configure to see multiple errors in response
    app.config['BUNDLE_ERRORS'] = True

    @app.route('/')
    @app.route('/ssd_api')
    def index():
        return get_documentation()

    @app.errorhandler(404)
    def not_found(error):
        return make_response(jsonify({'error': 'Not found'}), 404)
    
    # Flask_restful api
    api = Api(app)
    api.add_resource(TableNames, '/ssd_api/get_table')
    api.add_resource(GetTable, '/ssd_api/get_table/<string:table_name>')
    api.add_resource(GetTableCols, '/ssd_api/get_table_cols/')
    api.add_resource(GetDistinctX, '/ssd_api/get_distinct/')
    api.add_resource(FilterTableWithPTID, '/ssd_api/filter_table_with_ptid/')
    return app


if __name__ == '__main__': # pragma: no cover
    app = create_app()
    if sys.platform == 'linux':
        app.run(debug=False, port=config.getint('app', 'port'))
    else:
        app.run(debug=True, port=config.getint('app', 'port'))
