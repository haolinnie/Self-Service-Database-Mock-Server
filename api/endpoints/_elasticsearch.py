"""
Lightweight elasticsearch search-as-you-type proxy
"""
from datetime import datetime
from flask import Blueprint, request
from elasticsearch import Elasticsearch
import certifi

from api.models import db, models
from api.core import create_response, KEYWORDS, get_database_url
from api.auth import auth


_elasticsearch = Blueprint("_elasticsearch", __name__)

_es = Elasticsearch(
    get_database_url()["elasticsearch"], use_ssl=True, ca_certs=certifi.where()
)


def _generate_body(query):
    return {
        "query": {
            "multi_match": {
                "query": query,
                "type": "bool_prefix",
                "fields": ["name", "name._2gram", "name._3gram"],
            }
        }
    }


@_elasticsearch.route("/ssd_api/es/<index>", methods=["GET"])
def es_search(index):
    query = request.args["query"]
    res = _es.search(index=index, body=_generate_body(query))
    matches = [v.get("_source").get("name") for v in res.get("hits").get("hits")]
    return create_response(data={"matches": matches})
