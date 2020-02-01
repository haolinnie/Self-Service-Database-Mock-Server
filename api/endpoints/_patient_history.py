from flask import Blueprint, request

from api.models import db
from api.auth import auth
from api.core import (
    create_response,
    KEYWORDS,
    _generate_like_or_filters,
    _to_list_of_dict,
)
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

_patient_history = Blueprint("_patient_history", __name__)


@_patient_history.route("/ssd_api/patients", methods=["GET"])
@auth.login_required
def patients():
    arg_pt_ids = request.args.getlist("pt_id")

    pt_ids = pt_deid.query.filter(pt_deid.pt_id.in_(arg_pt_ids)).all()

    out_json = {}
    med_cols = ("id", "generic_name", "therapeutic_class", "date")
    diag_cols = ("diagnosis", "date")
    lab_cols = ("lab_name", "lab_value", "unit", "date")
    smart_cols = ("name", "value", "smart_data_id", "date")

    for curr_id in pt_ids:
        curr_id_str = str(curr_id.pt_id)

        # Initialise dict for current pt_id
        out_json[curr_id_str] = {}

        # Medication
        res = (
            curr_id.medication_deid.with_entities(
                medication_deid.medication_id,
                medication_deid.generic_name,
                medication_deid.therapeutic_class,
                medication_deid.order_placed_dt,
            )
            .order_by(medication_deid.order_placed_dt.desc())
            .all()
        )
        out_json[curr_id_str]["medication"] = _to_list_of_dict(res, med_cols)

        # Eye Diagnosis
        def _filter_diagnosis(systemic=True):
            or_filters = _generate_like_or_filters(
                diagnosis_deid.diagnosis_name,
                KEYWORDS["eye_diagnosis_keywords"],
                unlike=systemic,
            )
            return (
                curr_id.diagnosis_deid.with_entities(
                    diagnosis_deid.diagnosis_name, diagnosis_deid.diagnosis_start_dt
                )
                .filter(db.or_(*or_filters))
                .order_by(diagnosis_deid.diagnosis_start_dt.desc())
                .all()
            )

        res = _filter_diagnosis(systemic=False)
        out_json[curr_id_str]["eye_diagnosis"] = dict(res)

        # Systemic Diagnosis
        res = _filter_diagnosis(systemic=True)
        out_json[curr_id_str]["systemic_diagnosis"] = dict(res)

        # Lab values
        res = (
            curr_id.lab_value_deid.with_entities(
                lab_value_deid.name,
                lab_value_deid.value,
                lab_value_deid.reference_unit,
                lab_value_deid.result_dt,
            )
            .order_by(lab_value_deid.result_dt.desc())
            .all()
        )

        out_json[curr_id_str]["lab_values"] = _to_list_of_dict(res, lab_cols)

        # Vision
        res = smart_data_deid.get_data_for_pt_id(curr_id.pt_id, vision=True)
        out_json[curr_id_str]["vision"] = _to_list_of_dict(res, smart_cols)

        # Pressure
        res = smart_data_deid.get_data_for_pt_id(curr_id.pt_id, pressure=True)
        out_json[curr_id_str]["pressure"] = _to_list_of_dict(res, smart_cols)

        # Image types
        out_json[curr_id_str]["image_type"] = image_deid.get_image_procedure_from_pt_id(
            curr_id.pt_id
        )

    return create_response(data=out_json)
