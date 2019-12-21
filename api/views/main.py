from flask import Blueprint, request, render_template

from api import db as db_utils
from api.db import Database

from flask import (
    jsonify,
)  ## This should be removed later after creating a make_response function


main = Blueprint("main", __name__)


@main.route("/")
@main.route("/ssd_api", methods=["GET"])
def index():
    return render_template("debug.html")


@main.errorhandler(404)
def not_found(error):
    return make_response(jsonify({"error": "Not found"}), 404)


@main.route("/ssd_api/get_table", methods=["GET"])
def get_table():
    return jsonify({"table_names": db_utils.get_table_names()})

