def test_get_table_names(client):
    res = client.get("/ssd_api/get_table")
    assert res.json["success"]


def test_get_cols(client):
    # Test endpoint
    res = client.get("/ssd_api/get_table_cols")
    assert res.json["success"] == False
    # Test successful GET
    res = client.get("/ssd_api/get_table_cols?table_name=pt_deid")
    assert res.json["success"]
    assert "table_name" in res.json["result"]
    assert res.json["result"]["table_name"] == "pt_deid"
    # Test injection
    res = client.get("/ssd_api/get_table_cols?table_name=some;injection")
    assert res.json["success"] == False
    # Test wrong table
    res = client.get("/ssd_api/get_table_cols?table_name=bla")
    assert res.json["success"]
    assert len(res.json["result"]["columns"]) == 0


def test_get_distinct(client):
    # Table name required
    res = client.get("/ssd_api/get_distinct")
    assert res.json["success"] == False

    # Successful GET
    res = client.get("/ssd_api/get_distinct?table_name=pt_deid&col_name=pt_id")
    assert res.json["success"]
    assert res.json["result"]["table_name"] == "pt_deid"

    # Missing col name
    res = client.get("/ssd_api/get_distinct?table_name=pt_deid")
    assert res.json["success"] == False

    # Missing table name
    res = client.get("/ssd_api/get_distinct?col_name=pt_id")
    assert res.json["success"] == False

    # Wrong column name
    res = client.get("/ssd_api/get_distinct?table_name=pt_deid&col_name=bla")
    assert res.json["success"] == False

    # Test injection
    res = client.get("/ssd_api/get_distinct?table_name=some;injection&col_name=in;a")
    assert res.json["success"] == False


def test_get_distinct_special(client):
    res = client.get("/ssd_api/get_distinct?special=eye_diagnosis")
    assert res.json["success"]
    assert res.json["result"]["special"] == "eye_diagnosis"

    res = client.get("/ssd_api/get_distinct?special=systemic_diagnosis")
    assert res.json["success"]

    res = client.get("/ssd_api/get_distinct?special=bla")
    assert res.json["success"] == False


def test_filter_table_with_ptid(client):
    # Require at least 1 pt_id
    res = client.get("/ssd_api/filter_table_with_ptid")
    assert res.json["success"] == False

    # Must provide table name
    res = client.get("/ssd_api/filter_table_with_ptid?pt_id=100")
    assert res.json["success"] == False

    # Single pt_id query
    res = client.get("/ssd_api/filter_table_with_ptid?pt_id=20676&table_name=pt_deid")
    assert res.json["success"]
    assert "columns" in res.json["result"]

    # Multi pt_id query
    res = client.get(
        "/ssd_api/filter_table_with_ptid?pt_id=20676&pt_id=36440&table_name=pt_deid"
    )
    assert res.json["success"]
    assert "columns" in res.json["result"]
