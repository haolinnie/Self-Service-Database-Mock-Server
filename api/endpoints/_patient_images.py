from flask import Blueprint, request

from api.models import db
from api.core import create_response, _to_list_of_dict
from api.auth import auth
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


@_patient_images.route("/ssd_api/patient_images", methods=["GET"])
@auth.login_required
def patient_images():
    arg_pt_ids = request.args.getlist("pt_id")
    pt_ids = pt_deid.query.filter(pt_deid.pt_id.in_(arg_pt_ids))

    out_json = {}

    image_cols = (
        "image_id",
        "image_num",
        "image_type",
        "image_laterality",
        "image_procedure_id",
    )
    img_prcdr_cache = dict(
        image_procedure.query.with_entities(
            image_procedure.image_procedure_id, image_procedure.image_procedure
        ).all()
    )

    for curr_id in pt_ids:

        curr_id_str = str(curr_id.pt_id)
        out_json[curr_id_str] = []

        curr_exams = curr_id.exam_deid.order_by(exam_deid.exam_date.desc()).all()

        for curr_exam in curr_exams:
            curr_exam_json = {
                "exam_id": curr_exam.exam_id,
                "exam_date": curr_exam.exam_date,
                "images": {},
            }

            res = (
                curr_exam.image_deid.with_entities(
                    image_deid.image_id,
                    image_deid.image_num,
                    image_deid.image_type,
                    image_deid.image_laterality,
                    image_deid.image_procedure_id,
                )
                .order_by(image_deid.image_num)
                .all()
            )

            temp = [
                dict(zip(image_cols, list(v[:-1]) + [img_prcdr_cache[v[-1]]]))
                for v in res
            ]

            curr_exam_json["images"] = _to_list_of_dict(res, image_cols)
            out_json[curr_id_str].append(curr_exam_json)

    return create_response(data=out_json)
