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

    A query is constructed for each separate table other than pt_deid, thereby
    avoiding multiple joins which significantly slows down the search.
    """
    data = json.loads(request.data.decode())["filters"]

    # Create BaseQuery object
    qry = db.session.query(models["pt_deid"])
    # Create pt_ids set with all pt_ids
    pt_ids = set([v.pt_id for v in qry.all()])
    # Get current time for age calculation and profiling
    td = datetime.today()

    if "age" in data or "ethnicity" in data:
        qry = db.session.query(models["pt_deid"])
        # Get age constraints
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

            del data["age"] # might be unecessary to free this memory

            qry = qry.filter(models["pt_deid"].dob < data["dob"]["older_than"]).filter(
                models["pt_deid"].dob > data["dob"]["younger_than"]
            )

        # Get ethnicity constraints
        if "ethnicity" in data:
            qry = db.session.query(models["pt_deid"])
            qry = qry.filter(models["pt_deid"].ethnicity.in_(data["ethnicity"]))

        pt_ids = pt_ids.intersection([v.pt_id for v in qry.all()])

    # Get eye diagnosis
    if "eye_diagnosis" in data:
        """This currently uses OR logic, compared to AND
        """
        qry = db.session.query(models["pt_deid"])
        qry = qry.join(models["diagnosis_deid"]).filter(
            models["diagnosis_deid"].diagnosis_name.in_(data["eye_diagnosis"])
        )
        pt_ids = pt_ids.intersection([v.pt_id for v in qry.all()])

    # Get systemic diagnosis
    if "systemic_diagnosis" in data:
        """This currently uses OR logic, compared to AND
        """
        qry = db.session.query(models["pt_deid"])
        qry = qry.join(models["diagnosis_deid"]).filter(
            models["diagnosis_deid"].diagnosis_name.in_(data["systemic_diagnosis"])
        )
        pt_ids = pt_ids.intersection([v.pt_id for v in qry.all()])

    # Get image procedure type
    if "image_procedure_type" in data:
        """TODO: This filter with 2 joins is quite slow - needs improvement
        """
        assert type(data["image_procedure_type"]) == list
        qry = db.session.query(models["pt_deid"])
        qry = qry.join(models["image_deid"]).join(models["image_procedure"])
        and_query = [
            models["image_procedure"].image_procedure == img_proc_type
            for img_proc_type in data["image_procedure_type"]
        ]
        qry = qry.filter(db.and_(*and_query))
        pt_ids = pt_ids.intersection([v.pt_id for v in qry.all()])

    # Labs
    # TODO:
    

    # Medication_generic_name
    if "medication_generic_name" in data:
        """Currently using OR instead of AND logic
        """
        qry = db.session.query(models["pt_deid"])
        qry = qry.join(models["medication_deid"])
        qry = qry.filter(
            models["medication_deid"].generic_name.in_(data["medication_generic_name"])
        )
        pt_ids = pt_ids.intersection([v.pt_id for v in qry.all()])

    # Medication therapeutic class
    if "medication_therapeutic_class" in data:
        """Currently using OR instead of AND logic
        """
        qry = db.session.query(models["pt_deid"])
        qry = qry.join(models["medication_deid"])
        qry = qry.filter(
            models["medication_deid"].therapeutic_class.in_(
                data["medication_therapeutic_class"]
            )
        )
        pt_ids = pt_ids.intersection([v.pt_id for v in qry.all()])


    # Smart data
    if "left_vision" in data or "right_vision" in data or "left_pressure" in data or "right_pressure" in data:
        qry = db.session.query(models["pt_deid"])
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

        pt_ids = pt_ids.intersection([v.pt_id for v in qry.all()])

    return create_response(
        data={
            "pt_id": list( pt_ids ),
            "time_taken_seconds": (datetime.today() - td).total_seconds(),
        }
    )
