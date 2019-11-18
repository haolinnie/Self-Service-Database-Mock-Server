#!../flask/bin/python
import os
import sys
from flask import Flask, jsonify
from flask import make_response
from flask_restful import Resource, Api, reqparse

from ssd_api.util import get_documentation
from ssd_api.db_op import init_app, db_execute
from ssd_api.db_op import get_db, get_table_names, sqlite3
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

        med_cols = "*"
        cmd = """
        SELECT {}
        FROM {}
        WHERE pt_id IN({})
        ORDER BY pt_id
        """.format(med_cols, table_name, pt_id)

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


class PatientHistory(Resource):
    def get(self):
        data = parser.parse_args()
        pt_id = data.get('pt_id')

        if not pt_id:
            return {'ERROR': 'Must provide at least 1 pt_id'}

        out_json = {}
        med_cols = ('id', 'generic_name', 'therapeutic_class', 'date')
        diag_cols = ('diagnosis', 'date')
        lab_cols = ('lab_name', 'lab_value', 'unit', 'date')
        smart_cols = ('name', 'value', 'smart_data_id', 'date')
        for id in pt_id:
            # Initialise dict for current pt_id
            out_json[str(id)] = {}

            # Medication
            cols = "generic_name, therapeutic_class, order_placed_dt"
            table_name = "medication_deid"
            cmd = """ SELECT {} FROM {} WHERE pt_id IN({}) ORDER BY order_placed_dt
            """.format(cols, table_name, id)
            res = db_execute(cmd)
            out_json[str(id)]['medication'] = [dict(zip(med_cols, val)) for val in res]

            # Diagnosis
            cols = "diagnosis_name, diagnosis_start_dt"
            table_name = "diagnosis_deid"
            cmd = """ SELECT {} FROM {} WHERE pt_id IN({}) ORDER BY diagnosis_start_dt 
            """.format(cols, table_name, id)
            res = db_execute(cmd)
            out_json[str(id)]['eye_diagnosis'] = [dict(zip(diag_cols, val)) for val in res if val[0].find('retina')!=-1]
            out_json[str(id)]['systemic_diagnosis'] = [dict(zip(diag_cols, val)) for val in res if val[0].find('retina')==-1]

            # Lab values
            cols = "name, value, reference_unit,result_dt"
            table_name = "lab_value_deid"
            cmd = """ SELECT {} FROM {} WHERE pt_id IN({}) ORDER BY result_dt
            """.format(cols, table_name, id)
            res = db_execute(cmd)
            out_json[str(id)]['lab_values'] = [dict(zip(lab_cols, val)) for val in res]

            # Vision & Pressure
            cols = "element_name, smrtdta_elem_value, smart_data_id, value_dt"
            table_name = "smart_data_deid"
            cmd = """ SELECT {} FROM {} WHERE pt_id IN({}) ORDER BY value_dt
            """.format(cols, table_name, id)
            res = db_execute(cmd)
            out_json[str(id)]['vision'] = [dict(zip(smart_cols, val)) for val in res if val[0].find('ACUIT') != -1]
            out_json[str(id)]['pressure'] = [dict(zip(smart_cols, val)) for val in res if val[0].find('PRESSURE') != -1]

        return out_json


class PatientImages(Resource):
    def get(self):
        data = parser.parse_args()
        pt_id = data.get('pt_id')

        if not pt_id:
            return {'ERROR': 'Must provide at least 1 pt_id'}

        out_json = {}
        image_cols = ('image_id', 'image_num', 'image_type', 'image_laterality', 'image_procedure_id')
        
        ## image_procedures cache
        cmd = """SELECT image_procedure_id, image_procedure FROM image_procedure"""
        res = db_execute(cmd)
        image_procedures = dict(res)
        for id in pt_id:
            cmd = """ SELECT exam_id, exam_date FROM exam_deid
            WHERE pt_id IN({}) ORDER BY exam_date """.format(id)
            res = db_execute(cmd)
            out_cols = ('exam_id', 'exam_date')
            out_json[str(id)] = [dict(zip(out_cols, val)) for val in res]

            for curr_exam in out_json[str(id)]:
                curr_exam['images'] = {}
                cmd = """ SELECT image_id, image_num, image_type, image_laterality, image_procedure_id
                FROM image_deid WHERE exam_id IN({}) ORDER BY image_num """.format(curr_exam['exam_id'])
                res = db_execute(cmd)
                curr_exam['images'] = [dict(zip(image_cols, list(val[:-1]) + [image_procedures[val[-1]]] )) for val in res]

        return out_json


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
    api.add_resource(GetTableCols, '/ssd_api/get_table_cols')
    api.add_resource(GetDistinctX, '/ssd_api/get_distinct')
    api.add_resource(FilterTableWithPTID, '/ssd_api/filter_table_with_ptid')

    api.add_resource(PatientHistory, '/ssd_api/patients') ## Patient history
    api.add_resource(PatientImages, '/ssd_api/patient_images') 

    return app


if __name__ == '__main__': # pragma: no cover
    app = create_app()
    app.run(debug=True, port=config.getint('app', 'port'))