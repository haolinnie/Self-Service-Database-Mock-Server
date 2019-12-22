import json
from datetime import datetime
from flask import Blueprint, request, render_template, jsonify

from api import db as db_utils
from api.db import Database
from api.core import create_response, check_sql_safe


main = Blueprint("main", __name__)


@main.route("/local_debug")
def local_debug():
    breakpoint()
    return "<h1>Hello World</h1>"


@main.route("/")
@main.route("/ssd_api", methods=["GET"])
def index():
    return render_template("debug.html")


@main.route("/ssd_api/get_table", methods=["GET"])
def get_table():
    return create_response(data={"table_names": db_utils.get_table_names()})


@main.route("/ssd_api/get_table_cols", methods=["GET"])
def get_table_cols():

    if "table_name" not in request.args:
        return create_response(message="table_name missing", status=420)
    table_name = request.args["table_name"]

    if not check_sql_safe(table_name):  # Prevent Injection
        return create_response(message="Invalid input", status=420)

    try:
        col_names = db_utils.get_table_columns(table_name)
    except Exception as e:
        return create_response(message=str(e), status=420)

    return create_response(data={"table_name": table_name, "columns": col_names})


@main.route("/ssd_api/get_distinct", methods=["GET"])
def get_distinct():
    """Get distinct values given a table_name and col_name
    special can be used to get eye_diagnosis and systemic_diagnosis
    """
    if "special" not in request.args:
        col_name = request.args["col_name"]
        table_name = request.args["table_name"]

        if not check_sql_safe(table_name, col_name):  # Prevent Injection
            return create_response(message="Invalid input", status=420)

        try:
            cmd = "SELECT DISTINCT {} FROM {}".format(col_name, table_name)
            data = db_utils.db_execute(cmd)
            data = [r[0] for r in data if r[0]]
        except Exception as e:
            return create_response(message=str(e), status=420)

        return create_response(
            data={"data": data, "table_name": table_name, "col_name": col_name,}
        )

    else:
        special = request.args["special"]
        if special == "eye_diagnosis":
            col_name = special
            cmd = r"""SELECT DISTINCT diagnosis_name FROM diagnosis_deid WHERE 
            (diagnosis_name LIKE '%retina%' OR diagnosis_name LIKE '%macula%'
            OR diagnosis_name LIKE '%opia%' OR diagnosis_name LIKE '%iri%')
            ORDER BY diagnosis_name;"""
            data = db_utils.db_execute(cmd)
            data = [r[0] for r in data]
        elif special == "systemic_diagnosis":
            col_name = special
            cmd = r"""SELECT DISTINCT diagnosis_name FROM diagnosis_deid WHERE NOT
            (diagnosis_name LIKE '%retina%' OR diagnosis_name LIKE '%macula%'
            OR diagnosis_name LIKE '%opia%' OR diagnosis_name LIKE '%iri%')
            ORDER BY diagnosis_name;"""
            data = db_utils.db_execute(cmd)
            data = [r[0] for r in data if r[0]]
        else:
            return create_response(message="Special item not recognised", status=420)

        return create_response(data={"data": data, "special": special})


@main.route("/ssd_api/filter_table_with_ptid", methods=["GET"])
def filter_table_with_ptid():
    pt_id = request.args.getlist("pt_id")
    table_name = request.args["table_name"]

    ### Select values from tables with given pt_id
    pt_id = "'" + "', '".join([str(v) for v in pt_id]) + "'"

    med_cols = "*"
    cmd = """
    SELECT {}
    FROM {}
    WHERE pt_id IN({})
    ORDER BY pt_id
    """.format(
        med_cols, table_name, pt_id
    )

    # Filter table for pt_id
    try:
        with Database.get_db().cursor() as cursor:
            cursor.execute(cmd)
            col_names = list(map(lambda x: x[0], cursor.description))
            res = cursor.fetchall()
    except Exception as e:
        return create_response(message=str(e), status=420)

    return create_response(data={"columns": col_names, "data": res})


@main.route("/ssd_api/filter", methods=["POST"])
def filter():
    data = json.loads(request.data.decode())["filters"]

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

    # Create command that will query for age and ethnicity
    cmd = """SELECT pt_id FROM pt_deid where dob >= %s AND dob <= %s """
    # Get ethnicity constraints
    if "ethnicity" in data:
        # Append the ethnicity logic to the first command
        cmd += """ AND 
        ethnicity IN('{}""".format(
            "', '".join(data["ethnicity"]) + "')"
        )

    # Create pt_ids set HERE
    pt_ids = set(
        db_utils.db_execute(
            cmd, (data["dob"]["younger_than"], data["dob"]["older_than"])
        )
    )

    # Get eye and systemic diagnosis
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
        pt_ids = pt_ids.intersection(db_utils.db_execute(cmd))

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
        pt_ids = pt_ids.intersection(db_utils.db_execute(cmd))

    if len(pt_ids) == 0:
        return create_response(
            data={
                "pt_id": [],
                "time_taken_seconds": (datetime.today() - td).total_seconds(),
            }
        )

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
            pt_ids = pt_ids.intersection(db_utils.db_execute(cmd))
        except KeyError:  # medication_generic_name was not selected
            pass

        try:
            cmd = """SELECT pt_id FROM medication_deid WHERE """
            cmd += """therapeutic_class IN('{}""".format(
                "', '".join(data["medication_therapeutic_class"]) + "')"
            )
            pt_ids = pt_ids.intersection(db_utils.db_execute(cmd))
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
        pt_ids = pt_ids.intersection(db_utils.db_execute(cmd))

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
        pt_ids = pt_ids.intersection(db_utils.db_execute(cmd))

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
        pt_ids = pt_ids.intersection(db_utils.db_execute(cmd))

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
        pt_ids = pt_ids.intersection(db_utils.db_execute(cmd))

    return create_response(
        data={
            "pt_id": [] if len(pt_ids) == 0 else [v[0] for v in pt_ids],
            "time_taken_seconds": (datetime.today() - td).total_seconds(),
        }
    )


@main.route("/ssd_api/patients", methods=["GET"])
def patients():
    pt_id = request.args.getlist("pt_id")

    out_json = {}
    med_cols = ("id", "generic_name", "therapeutic_class", "date")
    diag_cols = ("diagnosis", "date")
    lab_cols = ("lab_name", "lab_value", "unit", "date")
    smart_cols = ("name", "value", "smart_data_id", "date")
    for id in pt_id:
        # Initialise dict for current pt_id
        out_json[str(id)] = {}

        # Medication
        cols = "medication_id, generic_name, therapeutic_class, order_placed_dt"
        table_name = "medication_deid"
        cmd = """ SELECT {} FROM {} WHERE pt_id IN({}) ORDER BY order_placed_dt
        """.format(
            cols, table_name, id
        )
        res = db_utils.db_execute(cmd)
        out_json[str(id)]["medication"] = [dict(zip(med_cols, val)) for val in res]

        # Eye Diagnosis
        # NOTE: currently using a naive method of matching 'macula', 'retina' and 'opia'
        # to classify eye or systemic diagnosis. This is probably not robust.
        cmd = r"""SELECT diagnosis_name, diagnosis_start_dt
        FROM diagnosis_deid WHERE pt_id={} AND
        (diagnosis_name LIKE '%retina%' OR diagnosis_name LIKE '%macula%'
        OR diagnosis_name LIKE '%opia%' OR diagnosis_name LIKE '%iri%') 
        ORDER BY diagnosis_start_dt;""".format(
            id
        )
        out_json[str(id)]["eye_diagnosis"] = db_utils.db_execute(cmd)

        # Systemic Diagnosis
        cmd = r"""SELECT diagnosis_name, diagnosis_start_dt
        FROM diagnosis_deid WHERE pt_id IN({}) AND NOT
        (diagnosis_name LIKE '%retina%' OR diagnosis_name LIKE '%macula%'
        OR diagnosis_name LIKE '%myopi%' OR diagnosis_name LIKE '%iri%')
        ORDER BY diagnosis_start_dt;""".format(
            id
        )
        out_json[str(id)]["systemic_diagnosis"] = db_utils.db_execute(cmd)

        # Lab values
        cols = "name, value, reference_unit,result_dt"
        table_name = "lab_value_deid"
        cmd = """ SELECT {} FROM {} WHERE pt_id IN({}) ORDER BY result_dt
        """.format(
            cols, table_name, id
        )
        res = db_utils.db_execute(cmd)
        out_json[str(id)]["lab_values"] = [dict(zip(lab_cols, val)) for val in res]

        # Vision
        cols = "element_name, smrtdta_elem_value, smart_data_id, value_dt"
        table_name = "smart_data_deid"
        cmd = """ SELECT {} FROM {} WHERE pt_id IN({})
        AND element_name LIKE '%visual acuity%' ORDER BY value_dt
        """.format(
            cols, table_name, id
        )
        res = db_utils.db_execute(cmd)
        out_json[str(id)]["vision"] = [dict(zip(smart_cols, val)) for val in res]

        # Pressure
        cmd = """ SELECT {} FROM {} WHERE pt_id IN({})
        AND element_name LIKE '%intraocular pressure%' ORDER BY value_dt
        """.format(
            cols, table_name, id
        )
        res = db_utils.db_execute(cmd)
        out_json[str(id)]["pressure"] = [dict(zip(smart_cols, val)) for val in res]

        # Image types
        cmd = """ SELECT DISTINCT IP.image_procedure
        FROM image_deid ID INNER JOIN image_procedure IP
        ON ID.image_procedure_id = IP.image_procedure_id
        WHERE ID.pt_id = {};""".format(
            id
        )
        res = db_utils.db_execute(cmd)
        out_json[str(id)]["image_type"] = [v[0] for v in res]

    return create_response(data=out_json)


@main.route("/ssd_api/patient_images", methods=["GET"])
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
    res = db_utils.db_execute(cmd)
    image_procedures = dict(res)
    for id in pt_id:
        cmd = """SELECT exam_id, exam_date FROM exam_deid
        WHERE pt_id IN({}) ORDER BY exam_date """.format(
            id
        )
        res = db_utils.db_execute(cmd)
        out_cols = ("exam_id", "exam_date")
        out_json[str(id)] = [dict(zip(out_cols, val)) for val in res]

        for curr_exam in out_json[str(id)]:
            curr_exam["images"] = {}
            cmd = """SELECT image_id, image_num, image_type, image_laterality, image_procedure_id
            FROM image_deid WHERE exam_id IN({}) ORDER BY image_num """.format(
                curr_exam["exam_id"]
            )
            res = db_utils.db_execute(cmd)
            curr_exam["images"] = [
                dict(zip(image_cols, list(val[:-1]) + [image_procedures[val[-1]]]))
                for val in res
            ]

    return create_response(data=out_json)
