import json
from datetime import datetime
from flask import Blueprint, request

from api.models import db, pt_deid
from api.core import create_response, check_sql_safe


_filter = Blueprint("_filter", __name__)


@_filter.route("/ssd_api/filter", methods=["POST"])
def filter():
    data = json.loads(request.data.decode())["filters"]

    # Create BaseQuery object
    qry = db.session.query(pt_deid)

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

    qry = qry.filter(pt_deid.dob < data["dob"]["older_than"])
    qry = qry.filter(pt_deid.dob > data["dob"]["younger_than"])

    # Create command that will query for age and ethnicity
    cmd = """SELECT pt_id FROM pt_deid where dob >= {} AND dob <= {} """
    # Get ethnicity constraints
    if "ethnicity" in data:
        qry.filter(pt_deid.ethnicity.in_(data["ethnicity"]))

    # Create pt_ids set HERE
    breakpoint()
    pt_ids = set(
        db.session.execute(
            cmd, (data["dob"]["younger_than"], data["dob"]["older_than"])
        ).fetchall()
    )

    # Get eye and systemic diagnosis
    if "eye_diagnosis" in data:
        pass

    if "eye_diagnosis" in data or "systemic_diagnosis" in data:
        data["diagnosis_name"] = []
        try:
            data["diagnosis_name"] += data["eye_diagnosis"]
            del data["eye_diagnosis"]
        except KeyError:  ## eye_diagnosis doesn't exist, systemic_diagnosis must
            pass
        try:
            data["diagnosis_name"] += data["systemic_diagnosis"]
            del data["systemic_diagnosis"]
        except KeyError:  # 'systemic_diagnosis isn't selected
            pass

        cmd = """ SELECT DISTINCT pt_id FROM diagnosis_deid WHERE diagnosis_name IN('{}""".format(
            "', '".join(data["diagnosis_name"]) + "')"
        )
        pt_ids = pt_ids.intersection(db.session.execute(cmd).fetchall())

    # Get image procedure type
    # Does not need reformatting
    if "image_procedure_type" in data:
        assert type(data["image_procedure_type"]) == type([])
        cmd = """SELECT DISTINCT pt_id FROM
        image_deid ID INNER JOIN image_procedure IP
        ON ID.image_procedure_id = IP.image_procedure_id
        WHERE image_procedure IN('{}""".format(
            "', '".join(data["image_procedure_type"]) + "')"
        )
        pt_ids = pt_ids.intersection(db.session.execute(cmd).fetchall())

    # Labs
    # TODO:

    # Medication_generic_name
    # TODO: generic name and therapeutic class can be merged into one SQL call
    if "medication_generic_name" in data or "medication_therapeutic_class" in data:
        # Initialise command for medication query

        try:
            cmd = """SELECT pt_id FROM medication_deid WHERE """
            cmd += """generic_name IN('{}""".format(
                "', '".join(data["medication_generic_name"]) + "')"
            )
            pt_ids = pt_ids.intersection(db.session.execute(cmd).fetchall())
        except KeyError:  # medication_generic_name was not selected
            pass

        try:
            cmd = """SELECT pt_id FROM medication_deid WHERE """
            cmd += """therapeutic_class IN('{}""".format(
                "', '".join(data["medication_therapeutic_class"]) + "')"
            )
            pt_ids = pt_ids.intersection(db.session.execute(cmd).fetchall())
        except KeyError:  # medication_deid was not selected
            pass

    # left vision
    # TODO: Vision filtering for the 20/XXX scale is currently
    # based on character level comparason and is not robust.
    # Need to figure out a way to compare the fractions
    if "left_vision" in data:
        cmd = """SELECT pt_id FROM smart_data_deid WHERE 
                    element_name LIKE '%visual acuity%left%' """
        if "less" in data["left_vision"]:
            cmd += """AND smrtdta_elem_value >= '{}' """.format(
                data["left_vision"]["less"]
            )
        if "more" in data["left_vision"]:
            cmd += """AND smrtdta_elem_value <= '{}' """.format(
                data["left_vision"]["more"]
            )
        cmd += " ORDER BY value_dt"
        pt_ids = pt_ids.intersection(db.session.execute(cmd).fetchall())

    # right vision
    if "right_vision" in data:
        cmd = """SELECT pt_id FROM smart_data_deid WHERE 
                    element_name LIKE '%visual acuity%right%' """
        if "less" in data["right_vision"]:
            cmd += """AND smrtdta_elem_value >= '{}' """.format(
                data["right_vision"]["less"]
            )
        if "more" in data["right_vision"]:
            cmd += """AND smrtdta_elem_value <= '{}' """.format(
                data["right_vision"]["more"]
            )
        cmd += " ORDER BY value_dt"
        pt_ids = pt_ids.intersection(db.session.execute(cmd).fetchall())

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
