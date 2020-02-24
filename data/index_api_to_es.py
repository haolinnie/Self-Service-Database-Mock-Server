import requests
from requests.auth import HTTPBasicAuth

from elasticsearch import Elasticsearch

import pdb


API_BASE_URL = "https://tigernie.com/ssd_api/"
# ELASTIC_URL = "https://elastic.tigernie.com/ssd_index/"
ELASTIC_URL = "http://127.0.0.1:9200/"

es = Elasticsearch(ELASTIC_URL)


def get_(endpoint, username, password, **kw_args):
    url = API_BASE_URL + endpoint
    res = requests.get(url, auth=HTTPBasicAuth(username, password), **kw_args)
    if res.ok:
        return res.json()["result"]
    else:
        raise Exception("API call failed")


TOKEN = get_("token", "debug", "debug")["token"]


def get_endpoint(endpoint, **kw_args):
    return get_(endpoint, TOKEN, "nouse", **kw_args)


sys_diag = get_endpoint("get_distinct", params={"special": "systemic_diagnosis"})[
    "data"
]
eye_diag = get_endpoint("get_distinct", params={"special": "eye_diagnosis"})["data"]

sys_diag = [{"name": v} for v in sys_diag]
eye_diag = [{"name": v} for v in eye_diag]

# Ignore 400 caused by IndexAlreadyExistsException
es.indices.create(index="systemic_diagnosis", ignore=400)

for i, v in enumerate(sys_diag):
    es.index(index="systemic_diagnosis", id=i, body=v)

pdb.set_trace()
