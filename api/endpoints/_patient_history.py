from flask import Blueprint, request

from api.models import db
from api.core import create_response, check_sql_safe


_patient_history = Blueprint("_patient_history", __name__)


@_patient_history.route("/ssd_api/patients", methods=["GET"])
def patients():
    pt_id = request.args.getlist("pt_id")

    out_json = {}
    med_cols = ("id", "generic_name", "therapeutic_class", "date")
    diag_cols = ("diagnosis", "date")
    lab_cols = ("lab_name", "lab_value", "unit", "date")
    smart_cols = ("name", "value", "smart_data_id", "date")
    for id in pt_id:
        # Initialise dict for current pt_id
        out_json[str(id)] = {}

        # Medication
        cols = "medication_id, generic_name, therapeutic_class, order_placed_dt"
        table_name = "medication_deid"
        cmd = """ SELECT {} FROM {} WHERE pt_id IN({}) ORDER BY order_placed_dt
        """.format(
            cols, table_name, id
        )
        res = db.session.execute(cmd).fetchall()
        out_json[str(id)]["medication"] = [dict(zip(med_cols, val)) for val in res]

        # Eye Diagnosis
        # NOTE: currently using a naive method of matching 'macula', 'retina' and 'opia'
        # to classify eye or systemic diagnosis. This is probably not robust.
        cmd = r"""SELECT diagnosis_name, diagnosis_start_dt
        FROM diagnosis_deid WHERE pt_id={} AND
        (diagnosis_name LIKE '%retina%' OR diagnosis_name LIKE '%macula%'
        OR diagnosis_name LIKE '%opia%' OR diagnosis_name LIKE '%iri%') 
        ORDER BY diagnosis_start_dt;""".format(
            id
        )
        out_json[str(id)]["eye_diagnosis"] = dict(db.session.execute(cmd).fetchall())

        # Systemic Diagnosis
        cmd = r"""SELECT diagnosis_name, diagnosis_start_dt
        FROM diagnosis_deid WHERE pt_id IN({}) AND NOT
        (diagnosis_name LIKE '%retina%' OR diagnosis_name LIKE '%macula%'
        OR diagnosis_name LIKE '%myopi%' OR diagnosis_name LIKE '%iri%')
        ORDER BY diagnosis_start_dt;""".format(
            id
        )
        out_json[str(id)]["systemic_diagnosis"] = dict(
            db.session.execute(cmd).fetchall()
        )

        # Lab values
        cols = "name, value, reference_unit,result_dt"
        table_name = "lab_value_deid"
        cmd = """ SELECT {} FROM {} WHERE pt_id IN({}) ORDER BY result_dt
        """.format(
            cols, table_name, id
        )
        res = db.session.execute(cmd).fetchall()
        out_json[str(id)]["lab_values"] = [dict(zip(lab_cols, val)) for val in res]

        # Vision
        cols = "element_name, smrtdta_elem_value, smart_data_id, value_dt"
        table_name = "smart_data_deid"
        cmd = """ SELECT {} FROM {} WHERE pt_id IN({})
        AND element_name LIKE '%visual acuity%' ORDER BY value_dt
        """.format(
            cols, table_name, id
        )
        res = db.session.execute(cmd).fetchall()
        out_json[str(id)]["vision"] = [dict(zip(smart_cols, val)) for val in res]

        # Pressure
        cmd = """ SELECT {} FROM {} WHERE pt_id IN({})
        AND element_name LIKE '%intraocular pressure%' ORDER BY value_dt
        """.format(
            cols, table_name, id
        )
        res = db.session.execute(cmd).fetchall()
        out_json[str(id)]["pressure"] = [dict(zip(smart_cols, val)) for val in res]

        # Image types
        cmd = """ SELECT DISTINCT IP.image_procedure
        FROM image_deid ID INNER JOIN image_procedure IP
        ON ID.image_procedure_id = IP.image_procedure_id
        WHERE ID.pt_id = {};""".format(
            id
        )
        res = db.session.execute(cmd).fetchall()
        out_json[str(id)]["image_type"] = [v[0] for v in res]

    return create_response(data=out_json)

