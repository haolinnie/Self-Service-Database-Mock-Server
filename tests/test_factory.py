from api import create_app


def test_index(client):
    assert client.get("/").status_code == 200
    assert client.get("/ssd_api").status_code == 200


def test_unknown_url(client):
    res = client.get("/ssd_api/bla")
    assert res.status_code == 500
