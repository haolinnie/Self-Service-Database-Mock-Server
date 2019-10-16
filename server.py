#!flask/bin/python
import sys
from flask import Flask, jsonify, Markup
from flask import make_response
from flask_restful import Resource, Api, reqparse
from flask_misaka import markdown

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

# Parse Documentation
with open('APIDocumentation.md', 'r') as f:
    content = f.read()
    readme = markdown(content)
    readme += Markup(
        """
        <meta charset=UTF-8>
        <meta name=viewport content="width=device-width,shrink-to-fit=0,user-scalable=no,minimum-scale=1,maximum-scale=1">
        <meta name=author content="Tiger Nie">
        <title>SSD API Docs</title>
        <style> html{font-family:"Courier New", Courier, monospace} body{padding-left:1rem;padding-right:1rem;}
        h3{font-weight:bold}code{background-color:rgb(246,248,250);display:block;padding:10px;} </style>
        """
    )


@app.route('/')
@app.route('/ssd_api/')
def index():
    return readme


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


class TableNames(Resource):
    def get(self):
        return {'table_names': TABLE_NAMES}


class GetTable(Resource):
    def get(self, table_name):
        # If no table name specified
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


api.add_resource(TableNames, '/ssd_api/get_table/')
api.add_resource(GetTable, '/ssd_api/get_table/<string:table_name>')
api.add_resource(GetTableCols, '/ssd_api/get_table_cols/')


if __name__ == '__main__':
    if sys.platform == 'linux':
        app.run(debug=False, port=5100)
    else:
        app.run(debug=True, port=5100)
