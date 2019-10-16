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
    TABLE_NAMES = cursor.fetchall()
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


todos = {
    'todo1': ['hello', 'world']
}


class TodoSimple(Resource):
    def get(self, todo_id):
        return {todo_id: todos[todo_id]}

    def put(self, todo_id):
        todos[todo_id] = request.form['data']
        return {todo_id: todos[todo_id]}


class TableNames(Resource):
    def get(self):
        return {'table_names': TABLE_NAMES}


class GetTable(Resource):
    def get(self):
        data = parser.parse_args()
        table_name = data.get('table_name')
        if table_name is None:
            return {'table_names': TABLE_NAMES}

        # Get column names of a table
        with get_db() as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM "+table_name)
            names = list(map(lambda x: x[0], cursor.description))
            cursor.close()

        res = {table_name: names}
        return res


api.add_resource(TodoSimple, '/api/todo/<string:todo_id>')
api.add_resource(TableNames, '/api/table_names/')
api.add_resource(GetTable, '/api/get_table/')


if __name__ == '__main__':
    app.run(debug=True)
