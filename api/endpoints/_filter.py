import json
from datetime import datetime
from flask import Blueprint, request

from api.models import db, models
from api.core import create_response, KEYWORDS


_filter = Blueprint("_filter", __name__)


@_filter.route("/ssd_api/filter", methods=["GET"])
def filter_get():
    return create_response(
        message="Please use the POST method to submit a query", status=420
    )


@_filter.route("/ssd_api/filter", methods=["POST"])
def filter_post():
    """Endpoint that response to filter POST requests
    This endpoint heavily utilises SQLAlchemy's Object Relational Mapper (ORM),
    allowing us to avoid explicitly writing SQL code, which seems to be the norm in applications.

    All filter parameters are chained into one query call using SQLAlchemy's 
    declarative pattern.
    """
    data = json.loads(request.data.decode())["filters"]

    # Create BaseQuery object
    qry = db.session.query(models["pt_deid"])

    # Get age constraints
    td = datetime.today()
    if "age" in data:
        # construct dob object to store SQL searchable data
        data["dob"] = {
            "younger_than": datetime(year=1900, month=1, day=1),
            "older_than": td,
        }
        if "less" in data["age"]:
            data["dob"]["younger_than"] = datetime(
                year=td.year - data["age"]["less"],
                month=td.month,
                day=td.day - 1 if td.month == 2 and td.day == 29 else td.day,
            )
        if "more" in data["age"]:
            data["dob"]["older_than"] = datetime(
                year=td.year - data["age"]["more"],
                month=td.month,
                day=td.day - 1 if td.month == 2 and td.day == 29 else td.day,
            )
        del data["age"]

        # Do the actual query
        qry = qry.filter(models["pt_deid"].dob < data["dob"]["older_than"]).filter(
            models["pt_deid"].dob > data["dob"]["younger_than"]
        )

    # Get ethnicity constraints
    if "ethnicity" in data:
        qry = qry.filter(models["pt_deid"].ethnicity.in_(data["ethnicity"]))

    # Get eye and systemic diagnosis
    data["diagnosis_name"] = []
    and_query = []
    if "eye_diagnosis" in data:
        # TODO: fix this so it's AND instead of OR
        # for diag in data["eye_diagnosis"]:
        #     and_query.append(models["diagnosis_deid"].diagnosis_name == diag)
        data["diagnosis_name"].append(*data["eye_diagnosis"])

    if "systemic_diagnosis" in data:
        data["diagnosis_name"].append(*data["systemic_diagnosis"])

    qry = qry.join(models["diagnosis_deid"]).filter(
        models["diagnosis_deid"].diagnosis_name.in_(data["diagnosis_name"])
    )

    # Get image procedure type
    # Does not need reformatting
    if "image_procedure_type" in data:
        assert type(data["image_procedure_type"]) == list
        qry = qry.join(models["image_deid"]).filter(
            models["image_procedure"].image_procedure.in_(data["image_procedure_type"])
        )

    # Labs
    # TODO:

    # Medication_generic_name
    qry = qry.join(models["medication_deid"])
    if "medication_generic_name" in data:
        qry = qry.filter(
            models["medication_deid"].generic_name.in_(data["medication_generic_name"])
        )

    # Medication therapeutic class
    if "medication_therapeutic_class" in data:
        qry = qry.filter(
            models["medication_deid"].therapeutic_class.in_(
                data["medication_therapeutic_class"]
            )
        )

    # Join the smart data deid table
    qry = qry.join(models["smart_data_deid"])
    # left vision
    # TODO: Vision filtering for the 20/XXX scale is currently
    # based on character level comparason and is not robust.
    # Need to figure out a way to compare the fractions
    if "left_vision" in data:
        and_query = [
            models["smart_data_deid"].element_name.ilike(KEYWORDS["left_vision"])
        ]
        if "less" in data["left_vision"]:
            and_query.append(
                models["smart_data_deid"].smrtdta_elem_value
                >= data["left_vision"]["less"]
            )
        if "more" in data["left_vision"]:
            and_query.append(
                models["smart_data_deid"].smrtdta_elem_value
                <= data["left_vision"]["more"]
            )
        qry = qry.filter(db.and_(*and_query))

    # right vision
    if "right_vision" in data:
        and_query = [
            models["smart_data_deid"].element_name.ilike(KEYWORDS["right_vision"])
        ]
        if "less" in data["right_vision"]:
            and_query.append(
                models["smart_data_deid"].smrtdta_elem_value
                >= data["right_vision"]["less"]
            )
        if "more" in data["right_vision"]:
            and_query.append(
                models["smart_data_deid"].smrtdta_elem_value
                <= data["right_vision"]["more"]
            )
        qry = qry.filter(db.and_(*and_query))

    # left pressure
    if "left_pressure" in data:
        and_query = [
            models["smart_data_deid"].element_name.ilike(KEYWORDS["left_pressure"])
        ]
        if "less" in data["left_pressure"]:
            and_query.append(
                models["smart_data_deid"].smrtdta_elem_value
                <= data["left_pressure"]["less"]
            )
        if "more" in data["left_pressure"]:
            and_query.append(
                models["smart_data_deid"].smrtdta_elem_value
                >= data["left_pressure"]["more"]
            )
        qry = qry.filter(db.and_(*and_query))

    # right pressure
    if "right_pressure" in data:
        and_query = [
            models["smart_data_deid"].element_name.ilike(KEYWORDS["right_pressure"])
        ]
        if "less" in data["right_pressure"]:
            and_query.append(
                models["smart_data_deid"].smrtdta_elem_value
                <= data["right_pressure"]["less"]
            )
        if "more" in data["right_pressure"]:
            and_query.append(
                models["smart_data_deid"].smrtdta_elem_value
                >= data["right_pressure"]["more"]
            )
        qry = qry.filter(db.and_(*and_query))

    pt_ids = [v.pt_id for v in qry.all()]
    return create_response(
        data={
            "pt_id": pt_ids,
            "time_taken_seconds": (datetime.today() - td).total_seconds(),
        }
    )
