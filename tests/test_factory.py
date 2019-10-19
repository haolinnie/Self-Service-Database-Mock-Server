from ssd_api import create_app


def test_config():
    assert not create_app().testing
    assert create_app({'TESTING': True}).testing


def test_doc(client):
    assert client.get('/').status_code == 200
    assert client.get('/ssd_api').status_code == 200

def test_404(client):
    res = client.get('/ssd_api/bla')
    assert res.status_code == 404
    assert res.data == b'{\n  "error": "Not found"\n}\n'
