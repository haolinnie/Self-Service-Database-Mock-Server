from flask import Blueprint, request, render_template

from api.models import db
from api.core import create_response, _to_list_of_dict
from api.models import (
    pt_deid,
    diagnosis_deid,
    lab_value_deid,
    medication_deid,
    medication_deid,
    smart_data_deid,
    visit_movement_deid,
    image_deid,
    exam_deid,
    image_procedure,
)


_patient_images = Blueprint("_patient_images", __name__)

# TODO rewrite this with ORM


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
    for curr_id in pt_id:
        qry = (
            exam_deid.query.with_entities(exam_deid.exam_id, exam_deid.exam_date)
            .filter(exam_deid.pt_id == curr_id)
            .order_by(exam_deid.exam_date.desc())
        )
        res = qry.all()
        out_json[str(curr_id)] = _to_list_of_dict(res, ("exam_id", "exam_date"))

        for curr_exam in out_json[str(curr_id)]:
            curr_exam["images"] = {}
            qry = (
                image_deid.query.with_entities(
                    image_deid.image_id,
                    image_deid.image_num,
                    image_deid.image_laterality,
                    image_deid.image_procedure_id,
                )
                .filter(image_deid.exam_id == curr_exam["exam_id"])
                .order_by(image_deid.image_num)
            )
            res = qry.all()

            curr_exam["images"] = [
                dict(zip(image_cols, list(val[:-1]) + [image_procedures[val[-1]]]))
                for val in res
            ]

    return create_response(data=out_json)
