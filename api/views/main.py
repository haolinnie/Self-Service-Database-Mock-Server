from flask import Blueprint, request, render_template

from api import db as db_utils
from api.db import Database


main = Blueprint("main", __name__)


@main.route("/")
@main.route("/ssd_api")
def index():
    return render_template("debug.html")


@main.errorhandler(404)
def not_found(error):
    return make_response(jsonify({"error": "Not found"}), 404)

