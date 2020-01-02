from flask import Blueprint, request, render_template

from ..models import db
from ..core import create_response, check_sql_safe


_patient_images = Blueprint("_patient_images", __name__)


@_patient_images.route("/ssd_api/patient_images", methods=["GET"])
def patient_images():
    pt_id = request.args.getlist("pt_id")

    out_json = {}
    image_cols = (
        "image_id",
        "image_num",
        "image_type",
        "image_laterality",
        "image_procedure_id",
    )

    ## image_procedures cache
    cmd = """SELECT image_procedure_id, image_procedure FROM image_procedure"""
    res = db.session.execute(cmd).fetchall()
    image_procedures = dict(res)
    for id in pt_id:
        cmd = """SELECT exam_id, exam_date FROM exam_deid
        WHERE pt_id IN({}) ORDER BY exam_date """.format(
            id
        )
        res = db.session.execute(cmd).fetchall()
        out_cols = ("exam_id", "exam_date")
        out_json[str(id)] = [dict(zip(out_cols, val)) for val in res]

        for curr_exam in out_json[str(id)]:
            curr_exam["images"] = {}
            cmd = """SELECT image_id, image_num, image_type, image_laterality, image_procedure_id
            FROM image_deid WHERE exam_id IN({}) ORDER BY image_num """.format(
                curr_exam["exam_id"]
            )
            res = db.session.execute(cmd).fetchall()
            curr_exam["images"] = [
                dict(zip(image_cols, list(val[:-1]) + [image_procedures[val[-1]]]))
                for val in res
            ]

    return create_response(data=out_json)
