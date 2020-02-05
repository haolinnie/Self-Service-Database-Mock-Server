import json
from datetime import datetime
from typing import Tuple

from flask import Blueprint, request

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
from api.core import create_response
from api.auth import auth


_filter = Blueprint("_filter", __name__)


def _age_to_dob(age):
    td = datetime.today()
    return datetime(
        year=td.year - age,
        month=td.month,
        day=td.day - 1 if td.month == 2 and td.day == 29 else td.day,
    )


@_filter.route("/ssd_api/filter", methods=["GET"])
@auth.login_required
def filter_get():
    return create_response(
        message="Please use the POST method to submit a query", status=420
    )


@_filter.route("/ssd_api/filter", methods=["POST"])
@auth.login_required
def filter_post():
    """Endpoint that response to filter POST requests
    This endpoint heavily utilises SQLAlchemy's Object Relational Mapper (ORM),
    allowing us to avoid explicitly writing SQL code, which seems to be the norm in applications.

    A query is constructed for each separate table other than pt_deid, thereby
    avoiding multiple joins which significantly slows down the search.
    """
    data = json.loads(request.data.decode())["filters"]

    # Create pt_ids set with all pt_ids
    pt_ids = set(pt_deid.get_all_pt_ids())
    # Get current time for age calculation and profiling
    td = datetime.today()

    # Get age constraints
    if "age" in data:
        # construct dob object to store SQL searchable data
        data["dob"] = {
            "younger_than": datetime(year=1900, month=1, day=1),
            "older_than": td,
        }
        if "less" in data["age"]:
            data["dob"]["younger_than"] = _age_to_dob(data["age"]["less"])

        if "more" in data["age"]:
            data["dob"]["older_than"] = _age_to_dob(data["age"]["more"])

        curr_ids = pt_deid.get_pt_id_by_age_or_race_1(
            younger_than=data["dob"]["younger_than"],
            older_than=data["dob"]["older_than"],
        )
        pt_ids = pt_ids.intersection(curr_ids)

    # Ethnicity
    if "ethnicity" in data:
        curr_ids = pt_deid.get_pt_id_by_age_or_race_1(race_1=data["ethnicity"],)
        pt_ids = pt_ids.intersection(curr_ids)

    # Get eye diagnosis
    if "eye_diagnosis" in data:
        """This currently uses OR logic, compared to AND
        """
        curr_ids = diagnosis_deid.get_pt_id_by_diagnosis_names(data["eye_diagnosis"])
        pt_ids = pt_ids.intersection(curr_ids)

    # Get systemic diagnosis
    if "systemic_diagnosis" in data:
        """This currently uses OR logic, compared to AND
        """
        curr_ids = diagnosis_deid.get_pt_id_by_diagnosis_names(
            data["systemic_diagnosis"]
        )
        pt_ids = pt_ids.intersection(curr_ids)

    # Get image procedure type
    if "image_procedure_type" in data:
        """This uses AND logic
        """
        curr_ids = image_deid.get_pt_id_by_image_procedure_type(
            data["image_procedure_type"]
        )
        pt_ids = pt_ids.intersection(curr_ids)

    # Labs
    # TODO:

    # Medication_generic_name
    if "medication_generic_name" in data:
        """Currently using OR instead of AND logic
        """
        curr_ids = medication_deid.get_pt_id_by_generic_name(
            data["medication_generic_name"]
        )
        pt_ids = pt_ids.intersection(curr_ids)

    # Medication therapeutic class
    if "medication_therapeutic_class" in data:
        """Currently using OR instead of AND logic
        """
        curr_ids = medication_deid.get_pt_id_by_therapeutic_class(
            data["medication_therapeutic_class"]
        )
        pt_ids = pt_ids.intersection(curr_ids)

    ### Smart data
    # TODO: Figure out a robust way to send "less" and "more" data
    # Currently parsing the number after "/" and converting to Int, which
    # will break if someone sends in something else

    # Vision
    curr_ids = smart_data_deid.get_pt_id_by_vision(data)
    if curr_ids:
        pt_ids = pt_ids.intersection(curr_ids)

    # Pressure
    # BROKEN RIGHT NOW - RETURNS ALL PATIENTS - FIXME
    curr_ids = smart_data_deid.get_pt_id_by_pressure(data)
    if curr_ids:
        pt_ids = pt_ids.intersection(curr_ids)

    return create_response(
        data={
            "pt_id": list(pt_ids),
            "time_taken_seconds": (datetime.today() - td).total_seconds(),
        }
    )
