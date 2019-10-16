#!flask/bin/python
from flask import Flask, jsonify
from flask import make_response, abort
from flask_restful import Resource, Api, reqparse
import pandas as pd
import json

# Get sample database
from db_op import get_db

TABLE_NAMES = []
# Load all table names
with get_db() as connection:
    cursor = connection.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    TABLE_NAMES = list(map(lambda x: x[0], cursor.fetchall()))
    cursor.close()

app = Flask(__name__)
api = Api(app)
parser = reqparse.RequestParser()

parser.add_argument('table_name', type=str, help='ERROR: empty table name')
parser.add_argument('column', type=str, help='ERROR: column name empty')


@app.route('/')
@app.route('/api/')
def index():
    return "Self-Service Database Mock API"


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


class TableNames(Resource):
    def get(self):
        print(TABLE_NAMES)
        return {'table_names': TABLE_NAMES}


class GetTable(Resource):
    def get(self, table_name):
        # If no table name specified
        print(table_name)
        if table_name is None:
            return {'table_names': TABLE_NAMES}

        # Get table from db
        try:
            with get_db() as connection:
                cursor = connection.cursor()
                cursor.execute("SELECT * FROM "+table_name)
                names = list(map(lambda x: x[0], cursor.description))
                data = cursor.fetchall()
                cursor.close()
        except:  # TODO: figure out which exception this is
            return {"ERROR": "table doesn't exist."}

        return {'columns': names, 'data': data}


class GetTableCols(Resource):
    def get(self):
        data = parser.parse_args()
        table_name = data.get('table_name')

        # If no table name specified
        if table_name is None:
            return {'table_names': TABLE_NAMES}

        # Get table columns
        try:
            with get_db() as connection:
                cursor = connection.cursor()
                cursor.execute("SELECT * FROM "+table_name)
                names = list(map(lambda x: x[0], cursor.description))
                cursor.close()
        except:  # TODO: figure out which exception this is
            return {"ERROR": "table doesn't exist."}

        return {'columns': names}


api.add_resource(TableNames, '/api/get_table/')
api.add_resource(GetTable, '/api/get_table/<string:table_name>')
api.add_resource(GetTableCols, '/api/get_table_cols/')


if __name__ == '__main__':
    app.run(debug=True, port=5100)
