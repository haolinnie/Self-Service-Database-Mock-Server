from flask import Blueprint, request, render_template

from api import db as db_utils
from api.db import Database
from api.core import create_response, check_sql_safe


main = Blueprint("main", __name__)


@main.route("/local_debug")
def local_debug():
    breakpoint()
    return create_response(data={"debug": "debug"})


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

    col_names = db_utils.get_table_columns(table_name)

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

    cmd = """
    SELECT *
    FROM {}
    WHERE pt_id IN({})
    ORDER BY pt_id
    """.format(
        table_name, pt_id
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

