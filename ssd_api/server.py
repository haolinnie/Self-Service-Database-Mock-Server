#!../flask/bin/python
import os
import sys
from flask import Flask, jsonify, make_response
from flask_restful import Resource, Api, reqparse

from . import db as db_utils
from .db import Database
from . import config_module
from .util import get_documentation


# Initialise request parser
parser = reqparse.RequestParser()
parser.add_argument('table_name', type=str, help='ERROR: empty table name')
parser.add_argument('col_name', type=str, help='ERROR: empty column name')
parser.add_argument('pt_id', type=int, action='append', help='ERROR: empty pt_id_list')


class TableNames(Resource):
    def get(self):
        return jsonify({'table_names': db_utils.get_table_names()})


def check_sql_safe(*argv):
    for arg in argv:
        if ' ' in arg or ';' in arg or ',' in arg:
            return False
    return True


class GetTable(Resource):
    def get(self, table_name):

        if not check_sql_safe(table_name): # Prevent Injection
            return jsonify({'ERROR': 'Invalid input'})

        try:
            with Database.get_db().cursor() as cursor:
                cursor.execute("SELECT * FROM {}".format(table_name))
                names = list(map(lambda x: x[0], cursor.description))
                data = cursor.fetchall()
        except Exception as e:
            return {"Exception Type": str(type(e)),
                    "Args": str(e.args),
                    "__str__": str(e.__str__)}

        return jsonify({'columns': names, 'data': data})


class GetTableCols(Resource):
    def get(self):
        data = parser.parse_args()
        table_name = data.get('table_name')

        if table_name is None:
            return jsonify({'ERROR': 'Must provide table_name'})

        if not check_sql_safe(table_name): # Prevent Injection
            return jsonify({'ERROR': 'Invalid input'})

        try:
            col_names = db_utils.get_table_columns(table_name)
        except Exception as e:
            return {"Exception Type": str(type(e)),
                    "Args": str(e.args),
                    "__str__": str(e.__str__)}

        return jsonify({'table_name': table_name, 'columns': col_names})


class GetDistinctX(Resource):
    def get(self):
        data = parser.parse_args()
        col_name = data.get('col_name')
        table_name = data.get('table_name')

        # error handling
        if table_name is None:
            return {'ERROR': 'empty table_name'}
        if col_name is None:
            return {'ERROR': 'empty col_name'}

        if not check_sql_safe(table_name, col_name): # Prevent Injection
            return jsonify({'ERROR': 'Invalid input'})

        try:
            cmd = "SELECT DISTINCT {} FROM {}".format(col_name, table_name)
            data = db_utils.db_execute(cmd)
            data = [r[0] for r in data]
        except Exception as e:
            return {"Exception Type": str(type(e)),
                    "Args": str(e.args),
                    "__str__": str(e.__str__)}
        
        return jsonify({"data": data, "table_name": table_name, "col_name": col_name})


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
            with Database.get_db().cursor() as cursor:
                cursor.execute(cmd)
                col_names = list(map(lambda x: x[0], cursor.description))
                res = cursor.fetchall()
        except Exception as e:
            return {"Exception Type": str(type(e)),
                    "Args": str(e.args),
                    "__str__": str(e.__str__)}

        return jsonify({'columns': col_names, 'data': res})


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
            cols = "medication_id, generic_name, therapeutic_class, order_placed_dt"
            table_name = "medication_deid"
            cmd = """ SELECT {} FROM {} WHERE pt_id IN({}) ORDER BY order_placed_dt
            """.format(cols, table_name, id)
            res = db_utils.db_execute(cmd)
            out_json[str(id)]['medication'] = [dict(zip(med_cols, val)) for val in res]

            # Diagnosis
            cols = "diagnosis_name, diagnosis_start_dt"
            table_name = "diagnosis_deid"
            cmd = """ SELECT {} FROM {} WHERE pt_id IN({}) ORDER BY diagnosis_start_dt 
            """.format(cols, table_name, id)
            res = db_utils.db_execute(cmd)
            out_json[str(id)]['eye_diagnosis'] = [dict(zip(diag_cols, val)) for val in res if val[0].find('retina')!=-1]
            out_json[str(id)]['systemic_diagnosis'] = [dict(zip(diag_cols, val)) for val in res if val[0].find('retina')==-1]

            # Lab values
            cols = "name, value, reference_unit,result_dt"
            table_name = "lab_value_deid"
            cmd = """ SELECT {} FROM {} WHERE pt_id IN({}) ORDER BY result_dt
            """.format(cols, table_name, id)
            res = db_utils.db_execute(cmd)
            out_json[str(id)]['lab_values'] = [dict(zip(lab_cols, val)) for val in res]

            # Vision & Pressure
            cols = "element_name, smrtdta_elem_value, smart_data_id, value_dt"
            table_name = "smart_data_deid"
            cmd = """ SELECT {} FROM {} WHERE pt_id IN({}) ORDER BY value_dt
            """.format(cols, table_name, id)
            res = db_utils.db_execute(cmd)
            out_json[str(id)]['vision'] = [dict(zip(smart_cols, val)) for val in res if val[0].find('ACUIT') != -1]
            out_json[str(id)]['pressure'] = [dict(zip(smart_cols, val)) for val in res if val[0].find('PRESSURE') != -1]

        return jsonify(out_json)


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
        res = db_utils.db_execute(cmd)
        image_procedures = dict(res)
        for id in pt_id:
            cmd = """SELECT exam_id, exam_date FROM exam_deid
            WHERE pt_id IN({}) ORDER BY exam_date """.format(id)
            res = db_utils.db_execute(cmd)
            out_cols = ('exam_id', 'exam_date')
            out_json[str(id)] = [dict(zip(out_cols, val)) for val in res]

            for curr_exam in out_json[str(id)]:
                curr_exam['images'] = {}
                cmd = """SELECT image_id, image_num, image_type, image_laterality, image_procedure_id
                FROM image_deid WHERE exam_id IN({}) ORDER BY image_num """.format(curr_exam['exam_id'])
                res = db_utils.db_execute(cmd)
                curr_exam['images'] = [dict(zip(image_cols, list(val[:-1]) + [image_procedures[val[-1]]] )) for val in res]

        return jsonify(out_json)


def create_app(config=None):

    # Instantiate flask app
    app = Flask(__name__, instance_relative_config=True)
    Database.init_app(app)

    if config is not None:
        Database.test = config['test']
    Database.test = False 

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
    app.run(debug=True, port=5100)
