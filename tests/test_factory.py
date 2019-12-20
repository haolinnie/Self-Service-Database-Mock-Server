from api import create_app


def test_doc(client):
    assert client.get('/').status_code == 200
    assert client.get('/ssd_api').status_code == 200

def test_404(client):
    res = client.get('/ssd_api/bla')
    assert res.status_code == 404
