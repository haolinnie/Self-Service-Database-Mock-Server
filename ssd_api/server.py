#!../flask/bin/python
import os
import sys
import datetime
from flask import Flask, jsonify, make_response, render_template, request
from flask_restful import Resource, Api, reqparse
import json

from . import db as db_utils
from .db import Database
from . import config_module
from .util import get_documentation


# Initialise request parser
parser = reqparse.RequestParser()
parser.add_argument('table_name', type=str, help='ERROR: empty table name')
parser.add_argument('col_name', type=str, help='ERROR: empty column name')
parser.add_argument('pt_id', type=int, action='append', help='ERROR: empty pt_id_list')

parser.add_argument('')


class TableNames(Resource):
    def get(self):
        return jsonify({'table_names': db_utils.get_table_names()})


def check_sql_safe(*argv):
    for arg in argv:
        if ' ' in arg or ';' in arg or ',' in arg or '--' in arg:
            return False
    return True


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

        # TODO: Get rid of NULL data

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


tableColumns = {
    'diagnosis_deid': 'diagnosis_name'
}

class Filter(Resource):
    def get(self):
        return {'Warning': 'Please use the POST method to filter :)'}

    def post(self):
        data = json.loads(request.data.decode())['filters']

        # Get age constraints
        td = datetime.date.today()
        data['dob'] = {'younger_than': datetime.datetime(year=1900, month=1, day=1),
                       'older_than': td}
        if 'age' in data:
            if 'less' in data['age']:
                data['dob']['younger_than'] = datetime.datetime(
                    year=td.year-data['age']['less'], month=td.month,
                    day=td.day-1 if td.month==2 and td.day==29 else td.day
                )
            if 'more' in data['age']:
                data['dob']['older_than'] = datetime.datetime(
                    year=td.year-data['age']['more'], month=td.month,
                    day=td.day-1 if td.month==2 and td.day==29 else td.day
                )

            # TODO: Check with Kerem about other conditions
            del data['age']

        # Create command that will query for age and ethnicity
        cmd = '''SELECT pt_id FROM pt_deid where dob >= %s AND dob <= %s '''
        # Get ethnicity constraints
        if 'ethnicity' in data:
            # Append the ethnicity logic to the first command
            cmd += ''' AND 
            ethnicity IN('{}'''.format(
                "', '".join(data['ethnicity']) + "')"
            )

        # Create pt_ids set HERE
        pt_ids = set(db_utils.db_execute(cmd, (data['dob']['younger_than'], data['dob']['older_than'])))

        # Get eye and systemic diagnosis
        if 'eye_diagnosis' in data or 'systemic_diagnosis' in data:
            data['diagnosis_name'] = []
            try:
                data['diagnosis_name'] += data['eye_diagnosis'] 
                del data['eye_diagnosis']
            except KeyError: ## eye_diagnosis doesn't exist, systemic_diagnosis must
                pass
            try:
                data['diagnosis_name'] += data['systemic_diagnosis']
                del data['systemic_diagnosis']
            except KeyError: # 'systemic_diagnosis isn't selected
                pass
        
            cmd = ''' SELECT DISTINCT pt_id FROM diagnosis_deid WHERE diagnosis_name LIKE '{}'''.format(
                "' AND diagnosis_name LIKE '".join(data['diagnosis_name']) + "'"
            )
            pt_ids = pt_ids.intersection(db_utils.db_execute(cmd))

        
        # Get image procedure type
        # Does not need reformatting
        if 'image_procedure_type' in data:
            assert type(data['image_procedure_type']) == type([])
            cmd = '''SELECT DISTINCT pt_id FROM
            image_deid ID INNER JOIN image_procedure IP
            ON ID.image_procedure_id = IP.image_procedure_id
            WHERE image_procedure LIKE '{}'''.format(
                "' AND image_procedure LIKE '".join(data['image_procedure_type']) + "'"
            )
            pt_ids = pt_ids.intersection(db_utils.db_execute(cmd))

        # if len(pt_ids) == 0:
        #     return {'pt_id': None}

        # Labs
        # TODO:

        # Medication_generic_name
        # TODO: generic name and therapeutic class can be merged into one SQL call
        if 'medication_generic_name' in data or 'medication_therapeutic_class' in data:
            # Initialise command for medication query
            
            try:
                cmd = '''SELECT pt_id FROM medication_deid WHERE '''
                cmd += '''generic_name LIKE '{}'''.format(
                    "' AND generic_name LIKE '".join(data['medication_generic_name']) + "'"
                )
                pt_ids = pt_ids.intersection(db_utils.db_execute(cmd))
            except KeyError: # medication_generic_name was not selected
                pass

            try:
                cmd = '''SELECT pt_id FROM medication_deid WHERE '''
                cmd += '''therapeutic_class LIKE '{}'''.format(
                    "' AND therapeutic_class LIKE '".join(data['medication_therapeutic_class']) + "'"
                )
                pt_ids = pt_ids.intersection(db_utils.db_execute(cmd))
            except KeyError: # medication_deid was not selected
                pass


        # left vision
        # Currently looks for 'less' and 'more' keys
        if 'left_vision' in data:
            cmd = '''SELECT pt_id FROM SMART_DATA_DEID WHERE 
                     element_name LIKE '%visual acuity%left%' '''
            if 'less' in data['left_vision']:
                cmd += '''AND smrtdta_elem_value >= '{}' '''.format(data['left_vision']['less'])
            if 'more' in data['left_vision']:
                cmd += '''AND smrtdta_elem_value <= '{}' '''.format(data['left_vision']['more'])
            cmd += ' ORDER BY value_dt'
            pt_ids = pt_ids.intersection(db_utils.db_execute(cmd))

        # right vision
        if 'right_vision' in data:
            cmd = '''SELECT pt_id FROM SMART_DATA_DEID WHERE 
                     element_name LIKE '%visual acuity%right%' '''
            if 'less' in data['right_vision']:
                cmd += '''AND smrtdta_elem_value >= '{}' '''.format(data['right_vision']['less'])
            if 'more' in data['right_vision']:
                cmd += '''AND smrtdta_elem_value <= '{}' '''.format(data['right_vision']['more'])
            cmd += ' ORDER BY value_dt'
            pt_ids = pt_ids.intersection(db_utils.db_execute(cmd))

        # left pressure
        if 'left_pressure' in data:
            cmd = '''SELECT pt_id FROM SMART_DATA_DEID WHERE 
                     element_name LIKE '%intraocular pressure%left%' '''
            if 'less' in data['left_pressure']:
                cmd += '''AND smrtdta_elem_value <= '{}' '''.format(data['left_pressure']['less'])
            if 'more' in data['left_pressure']:
                cmd += '''AND smrtdta_elem_value >= '{}' '''.format(data['left_pressure']['more'])
            cmd += ' ORDER BY value_dt'
            pt_ids = pt_ids.intersection(db_utils.db_execute(cmd))

        # right pressure
        if 'right_pressure' in data:
            cmd = '''SELECT pt_id FROM SMART_DATA_DEID WHERE 
                     element_name LIKE '%intraocular pressure%right%' '''
            if 'less' in data['right_pressure']:
                cmd += '''AND smrtdta_elem_value <= '{}' '''.format(data['right_pressure']['less'])
            if 'more' in data['right_pressure']:
                cmd += '''AND smrtdta_elem_value >= '{}' '''.format(data['right_pressure']['more'])
            cmd += ' ORDER BY value_dt'
            pt_ids = pt_ids.intersection(db_utils.db_execute(cmd))

        filterReturn(data, pt_ids)
        return {'pt_id': pt_ids}


def filterReturn(data, pt_ids):
    keys = list(data.keys())
    breakpoint()
    


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

            # Eye Diagnosis
            # NOTE: currently using a naive method of matching 'macula', 'retina' and 'opia'
            # to classify eye or systemic diagnosis. This is probably not robust.
            cmd = r"""SELECT diagnosis_name, diagnosis_start_dt
            FROM diagnosis_deid WHERE pt_id={} AND
            (diagnosis_name LIKE '%retina%' OR diagnosis_name LIKE '%macula%'
            OR diagnosis_name LIKE '%opia%') ORDER BY diagnosis_start_dt;""".format(id)
            out_json[str(id)]['eye_diagnosis'] = db_utils.db_execute(cmd)

            # Systemic Diagnosis
            cmd = r"""SELECT diagnosis_name, diagnosis_start_dt
            FROM diagnosis_deid WHERE pt_id IN({}) AND NOT
            (diagnosis_name LIKE '%retina%' OR diagnosis_name LIKE '%macula%'
            OR diagnosis_name LIKE '%myopi%') ORDER BY diagnosis_start_dt;""".format(id)
            out_json[str(id)]['systemic_diagnosis'] = db_utils.db_execute(cmd)

            # Lab values
            cols = "name, value, reference_unit,result_dt"
            table_name = "lab_value_deid"
            cmd = """ SELECT {} FROM {} WHERE pt_id IN({}) ORDER BY result_dt
            """.format(cols, table_name, id)
            res = db_utils.db_execute(cmd)
            out_json[str(id)]['lab_values'] = [dict(zip(lab_cols, val)) for val in res]

            # Vision
            cols = "element_name, smrtdta_elem_value, smart_data_id, value_dt"
            table_name = "smart_data_deid"
            cmd = """ SELECT {} FROM {} WHERE pt_id IN({})
            AND element_name LIKE '%visual acuity%' ORDER BY value_dt
            """.format(cols, table_name, id)
            res = db_utils.db_execute(cmd)
            out_json[str(id)]['vision'] = [dict(zip(smart_cols, val)) for val in res]

            # Pressure
            cmd = """ SELECT {} FROM {} WHERE pt_id IN({})
            AND element_name LIKE '%intraocular pressure%' ORDER BY value_dt
            """.format(cols, table_name, id)
            res = db_utils.db_execute(cmd)
            out_json[str(id)]['pressure'] = [dict(zip(smart_cols, val)) for val in res]

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


def create_app(**config):

    # Instantiate flask app
    app = Flask(__name__, instance_relative_config=True)
    Database(**config)
    Database.init_app(app)

    # proxy support for Nginx
    from werkzeug.middleware.proxy_fix import ProxyFix
    app.wsgi_app = ProxyFix(app.wsgi_app)

    # Configure to see multiple errors in response
    app.config['BUNDLE_ERRORS'] = True

    @app.route('/')
    @app.route('/ssd_api')
    def index():
        # return get_documentation()
        return render_template('debug.html')

    @app.errorhandler(404)
    def not_found(error):
        return make_response(jsonify({'error': 'Not found'}), 404)
 
    # Flask_restful api
    api = Api(app)
    api.add_resource(TableNames, '/ssd_api/get_table')
    api.add_resource(GetTableCols, '/ssd_api/get_table_cols')
    api.add_resource(GetDistinctX, '/ssd_api/get_distinct')
    api.add_resource(FilterTableWithPTID, '/ssd_api/filter_table_with_ptid')

    api.add_resource(Filter, '/ssd_api/filter') ## Big filter endpoint
    api.add_resource(PatientHistory, '/ssd_api/patients') ## Patient history
    api.add_resource(PatientImages, '/ssd_api/patient_images') 

    return app


if __name__ == '__main__': # pragma: no cover
    app = create_app()
    app.run(debug=True, port=5100)
