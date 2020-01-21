def test_get_table_names(client):
    url = "/ssd_api/get_table"

    res = client.get(url)
    assert res.json["success"]


def test_get_cols(client):
    url = "/ssd_api/get_table_cols"

    # Test endpoint
    res = client.get(url)
    assert not res.json["success"]

    # Test successful GET
    res = client.get(url + "?table_name=pt_deid")
    assert res.json["success"]
    assert "table_name" in res.json["result"]
    assert res.json["result"]["table_name"] == "pt_deid"

    # Test injection
    res = client.get(url + "?table_name=some;injection")
    assert not res.json["success"]

    # Test wrong table
    res = client.get(url + "?table_name=bla")
    assert not res.json["success"]


def test_get_distinct(client):
    url = "/ssd_api/get_distinct"

    # Table name required
    res = client.get(url)
    assert not res.json["success"]

    # Successful GET
    res = client.get(url + "?table_name=pt_deid&col_name=pt_id")
    assert res.json["success"]
    assert res.json["result"]["table_name"] == "pt_deid"

    # Missing col name
    res = client.get(url + "?table_name=pt_deid")
    assert not res.json["success"]

    # Missing table name
    res = client.get(url + "?col_name=pt_id")
    assert not res.json["success"]

    # Unavailable column name
    res = client.get(url + "?table_name=pt_deid&col_name=bla")
    assert not res.json["success"]

    # Unavailable table name
    res = client.get(url + "?table_name=bla&col_name=bla")
    assert not res.json["success"]

    # Test injection
    res = client.get(url + "?table_name=some;injection&col_name=in;a")
    assert not res.json["success"]


def test_get_distinct_special(client):
    url = "/ssd_api/get_distinct"

    res = client.get(url + "?special=eye_diagnosis")
    assert res.json["success"]
    assert res.json["result"]["special"] == "eye_diagnosis"

    res = client.get(url + "?special=systemic_diagnosis")
    assert res.json["success"]

    res = client.get(url + "?special=bla")
    assert not res.json["success"]


def test_filter_table_with_ptid(client):
    url = "/ssd_api/filter_table_with_ptid"

    # Require at least 1 pt_id
    res = client.get(url)
    assert not res.json["success"]

    # Must provide table name
    res = client.get(url + "?pt_id=100")
    assert not res.json["success"]

    # Single pt_id query
    res = client.get(url + "?pt_id=20676&table_name=pt_deid")
    assert res.json["success"]
    assert "data" in res.json["result"]

    # Multi pt_id query
    res = client.get(url + "?pt_id=20676&pt_id=36440&table_name=pt_deid")
    assert res.json["success"]
    assert "data" in res.json["result"]

    # Fake table
    res = client.get(url + "?pt_id=123&table_name=fake_table")
    assert not res.json["success"]
