from datetime import datetime
from flask import Blueprint, request, render_template
from sqlalchemy import or_

from api.models import db, models
from api.core import create_response, KEYWORDS, _generate_like_or_filters


_main = Blueprint("_main", __name__)


@_main.route("/")
@_main.route("/ssd_api", methods=["GET"])
def index():
    return render_template("debug.html")


@_main.route("/ssd_api/get_table", methods=["GET"])
def get_table():
    return create_response(data={"table_names": list(models.keys())})


@_main.route("/ssd_api/get_table_cols", methods=["GET"])
def get_table_cols():

    if "table_name" not in request.args:
        return create_response(message="table_name missing", status=420)

    table_name = request.args["table_name"]
    col_names = models[table_name].__table__.columns.keys()

    return create_response(data={"table_name": table_name, "columns": col_names})


@_main.route("/ssd_api/get_distinct", methods=["GET"])
def get_distinct():
    """Get distinct values given a table_name and col_name
    special can be used to get eye_diagnosis and systemic_diagnosis
    """
    td = datetime.now()
    if "special" not in request.args:
        """Get distinct items from the given table column
        """
        col_name = request.args["col_name"]
        table_name = request.args["table_name"]

        if table_name not in models:
            return create_response(
                message="Table '{}' is not available.".format(table_name), status=420
            )

        try:
            data = (
                db.session.query(models[table_name].__dict__[col_name]).distinct().all()
            )
            data = [r[0] for r in data if r[0]]
        except Exception as e:
            return create_response(message=str(e), status=420)

        return create_response(
            data={
                "data": data,
                "table_name": table_name,
                "col_name": col_name,
                "time_taken_seconds": (datetime.today() - td).total_seconds(),
            }
        )

    else:
        """Get distinct eye_diagnosis or systemic_diagnosis
        """
        special = request.args["special"]
        tb = models["diagnosis_deid"]

        if special == "eye_diagnosis":
            # SQLAlchemy ilike guarantees case-insensitive
            or_filters = _generate_like_or_filters(
                tb.diagnosis_name, KEYWORDS["eye_diagnosis_keywords"]
            )
            qry = (
                db.session.query(tb.diagnosis_name).distinct().filter(or_(*or_filters))
            )
            data = qry.all()
            data = [r[0] for r in data]

        elif special == "systemic_diagnosis":

            or_filters = _generate_like_or_filters(
                tb.diagnosis_name, KEYWORDS["eye_diagnosis_keywords"], unlike=True
            )
            qry = (
                db.session.query(tb.diagnosis_name).distinct().filter(or_(*or_filters))
            )
            data = qry.all()
            data = [r[0] for r in data]
        else:
            return create_response(message="Special item not recognised", status=420)

        return create_response(
            data={
                "data": data,
                "special": special,
                "time_taken_seconds": (datetime.today() - td).total_seconds(),
            }
        )


@_main.route("/ssd_api/filter_table_with_ptid", methods=["GET"])
def filter_table_with_ptid():
    pt_id = request.args.getlist("pt_id")
    table_name = request.args["table_name"]

    try:
        tb = models[table_name]
        data = db.session.query(tb).filter(tb.pt_id.in_(pt_id)).all()
        data = [v.to_dict() for v in data]
    except Exception as e:
        return create_response(message=str(e), status=420)

    return create_response(data={"data": data})
