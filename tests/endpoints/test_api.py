class TestGetTable:
    url = "/ssd_api/get_table"

    def TestGet(self, client):
        res = client.get(self.url)
        assert res.json["success"]


class TestGetCols:
    url = "/ssd_api/get_table_cols"

    def test_no_param(self, client):
        # Test endpoint
        res = client.get(self.url)
        assert not res.json["success"]

    def test_with_table_name(self, client):
        # Test successful GET
        res = client.get(self.url + "?table_name=pt_deid")
        assert res.json["success"]
        assert "table_name" in res.json["result"]
        assert res.json["result"]["table_name"] == "pt_deid"

    def test_injection(self, client):
        res = client.get(self.url + "?table_name=some;injection")
        assert not res.json["success"]

    def test_na_table(self, client):
        res = client.get(self.url + "?table_name=bla")
        assert not res.json["success"]


class TestGetDistinct:
    url = "/ssd_api/get_distinct"

    def test_no_param(self, client):
        res = client.get(self.url)
        assert not res.json["success"]

    def test_missing_col_name(self, client):
        res = client.get(self.url + "?table_name=pt_deid")
        assert not res.json["success"]

    def test_table_name_and_col_name(self, client):
        res = client.get(self.url + "?table_name=pt_deid&col_name=pt_id")
        assert res.json["success"]
        assert res.json["result"]["table_name"] == "pt_deid"

    def test_na_col_name(self, client):
        # Unavailable column name
        res = client.get(self.url + "?table_name=pt_deid&col_name=bla")
        assert not res.json["success"]

    def test_na_table_name(self, client):
        # Unavailable table name
        res = client.get(self.url + "?table_name=bla&col_name=bla")
        assert not res.json["success"]

    def test_injection(self, client):
        # Test injection
        res = client.get(self.url + "?table_name=some;injection&col_name=in;a")
        assert not res.json["success"]


class TestGetDistinctSpecial:
    url = "/ssd_api/get_distinct"

    def test_eye_diagnosis(self, client):
        res = client.get(self.url + "?special=eye_diagnosis")
        assert res.json["success"]
        assert res.json["result"]["special"] == "eye_diagnosis"

    def test_systemic_diagnosis(self, client):
        res = client.get(self.url + "?special=systemic_diagnosis")
        assert res.json["success"]

    def test_na_special(self, client):
        res = client.get(self.url + "?special=bla")
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
