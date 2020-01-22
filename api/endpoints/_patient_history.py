from flask import Blueprint, request

from api.models import db
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


def _filter_diagnosis(curr_id: int, or_filters: list) -> list:
    """Helper function to filter the diagnosis_deid table with a patient id and keywords (eye or systemic diagnosis)
    """
    qry = diagnosis_deid.query.with_entities(
        diagnosis_deid.diagnosis_name, diagnosis_deid.diagnosis_start_dt
    )
    qry = qry.filter(db.and_(diagnosis_deid.pt_id == curr_id, db.or_(*or_filters)))
    qry = qry.order_by(diagnosis_deid.diagnosis_start_dt.desc())
    return qry.all()


@_patient_history.route("/ssd_api/patients", methods=["GET"])
def patients():
    pt_id = request.args.getlist("pt_id")

    out_json = {}
    med_cols = ("id", "generic_name", "therapeutic_class", "date")
    diag_cols = ("diagnosis", "date")
    lab_cols = ("lab_name", "lab_value", "unit", "date")
    smart_cols = ("name", "value", "smart_data_id", "date")
    for curr_id in pt_id:
        # Initialise dict for current pt_id
        out_json[str(curr_id)] = {}

        # Medication
        qry = (
            medication_deid.query.with_entities(
                medication_deid.medication_id,
                medication_deid.generic_name,
                medication_deid.therapeutic_class,
                medication_deid.order_placed_dt,
            )
            .filter(medication_deid.pt_id == curr_id)
            .order_by(medication_deid.order_placed_dt.desc())
        )

        out_json[str(curr_id)]["medication"] = _to_list_of_dict(qry.all(), med_cols)

        # Eye Diagnosis
        or_filters = _generate_like_or_filters(
            diagnosis_deid.diagnosis_name, KEYWORDS["eye_diagnosis_keywords"]
        )
        out_json[str(curr_id)]["eye_diagnosis"] = dict(
            _filter_diagnosis(curr_id, or_filters)
        )

        # Systemic Diagnosis
        or_filters = _generate_like_or_filters(
            diagnosis_deid.diagnosis_name,
            KEYWORDS["eye_diagnosis_keywords"],
            unlike=True,
        )
        out_json[str(curr_id)]["systemic_diagnosis"] = dict(
            _filter_diagnosis(curr_id, or_filters)
        )

        # Lab values
        qry = (
            lab_value_deid.query.with_entities(
                lab_value_deid.name,
                lab_value_deid.value,
                lab_value_deid.reference_unit,
                lab_value_deid.result_dt,
            )
            .filter(lab_value_deid.pt_id == curr_id)
            .order_by(lab_value_deid.result_dt.desc())
        )

        out_json[str(curr_id)]["lab_values"] = _to_list_of_dict(qry.all(), lab_cols)

        # Vision
        res = smart_data_deid.get_data_for_pt_id(pt_id, vision=True)
        out_json[str(curr_id)]["vision"] = _to_list_of_dict(res, smart_cols)

        # Pressure
        res = smart_data_deid.get_data_for_pt_id(pt_id, pressure=True)
        out_json[str(curr_id)]["pressure"] = _to_list_of_dict(res, smart_cols)

        # Image types
        out_json[str(curr_id)][
            "image_type"
        ] = image_deid.get_image_procedure_from_pt_id(curr_id)

    return create_response(data=out_json)
