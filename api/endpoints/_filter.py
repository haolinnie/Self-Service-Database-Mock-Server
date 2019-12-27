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
    data = json.loads(request.data.decode())["filters"]

    # Create BaseQuery object
    qry = db.session.query(models["pt_deid"].pt_id).distinct()

    # Get age constraints
    td = datetime.today()
    data["dob"] = {
        "younger_than": datetime(year=1900, month=1, day=1),
        "older_than": td,
    }
    if "age" in data:
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

    qry = qry.filter(models["pt_deid"].dob < data["dob"]["older_than"]).filter(
        models["pt_deid"].dob > data["dob"]["younger_than"]
    )

    # Get ethnicity constraints
    if "ethnicity" in data:
        qry = qry.filter(models["pt_deid"].ethnicity.in_(data["ethnicity"]))

    # Get eye and systemic diagnosis
    data["diagnosis_name"] = []
    if "eye_diagnosis" in data:
        data["diagnosis_name"].append(*data["eye_diagnosis"])

    if "systemic_diagnosis" in data:
        data["diagnosis_name"].append(*data["systemic_diagnosis"])

    qry = qry.filter(
        models["diagnosis_deid"].diagnosis_name.in_(data["diagnosis_name"])
    )

    # Get image procedure type
    # Does not need reformatting
    # if "image_procedure_type" in data:
    #     assert type(data["image_procedure_type"]) == type([])

    #     # TODO:
    #     qry.filter(models["image_deid"].join(models["image_procedure"]))

    #     cmd = """SELECT DISTINCT pt_id FROM
    #     image_deid ID INNER JOIN image_procedure IP
    #     ON ID.image_procedure_id = IP.image_procedure_id
    #     WHERE image_procedure IN('{}""".format(
    #         "', '".join(data["image_procedure_type"]) + "')"
    #     )
    #     pt_ids = pt_ids.intersection(db.session.execute(cmd).fetchall())

    # Labs
    # TODO:

    # Medication_generic_name
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

    breakpoint()
    # left vision
    # TODO: Vision filtering for the 20/XXX scale is currently
    # based on character level comparason and is not robust.
    # Need to figure out a way to compare the fractions
    if "left_vision" in data:
        qry = qry.filter(
            models["smart_data_deid"].element_name.ilike(KEYWORDS["left_vision"])
        ).order_by(models["smart_data_deid"].value_dt)

        breakpoint()
        if "less" in data["left_vision"]:
            qry = qry.filter(
                models["smart_data_deid"].smrtdata_elem_value
                >= data["left_vision"]["less"]
            )

        if "more" in data["left_vision"]:
            qry = qry.filter(
                models["smart_data_deid"].smrtdata_elem_value
                <= data["left_vision"]["more"]
            )
    breakpoint()

    # right vision
    if "right_vision" in data:
        qry = qry.filter(
            models["smart_data_deid"].element_name.ilike(KEYWORDS["right_vision"])
        ).order_by(models["smart_data_deid"].value_dt)

        if "less" in data["right_vision"]:
            qry = qry.filter(
                models["smart_data_deid"].smrtdata_elem_value
                >= data["right_vision"]["less"]
            )

        if "more" in data["right_vision"]:
            qry = qry.filter(
                models["smart_data_deid"].smrtdata_elem_value
                <= data["right_vision"]["more"]
            )
    breakpoint()

    # left pressure
    if "left_pressure" in data:
        cmd = """SELECT pt_id FROM smart_data_deid WHERE 
                    element_name LIKE '%intraocular pressure%left%' """
        if "less" in data["left_pressure"]:
            cmd += """AND smrtdta_elem_value <= '{}' """.format(
                data["left_pressure"]["less"]
            )
        if "more" in data["left_pressure"]:
            cmd += """AND smrtdta_elem_value >= '{}' """.format(
                data["left_pressure"]["more"]
            )
        cmd += " ORDER BY value_dt"
        pt_ids = pt_ids.intersection(db.session.execute(cmd).fetchall())

    # right pressure
    if "right_pressure" in data:
        cmd = """SELECT pt_id FROM smart_data_deid WHERE 
                    element_name LIKE '%intraocular pressure%right%' """
        if "less" in data["right_pressure"]:
            cmd += """AND smrtdta_elem_value <= '{}' """.format(
                data["right_pressure"]["less"]
            )
        if "more" in data["right_pressure"]:
            cmd += """AND smrtdta_elem_value >= '{}' """.format(
                data["right_pressure"]["more"]
            )
        cmd += " ORDER BY value_dt"
        pt_ids = pt_ids.intersection(db.session.execute(cmd).fetchall())

    return create_response(
        data={
            "pt_id": [] if len(pt_ids) == 0 else [v[0] for v in pt_ids],
            "time_taken_seconds": (datetime.today() - td).total_seconds(),
        }
    )
