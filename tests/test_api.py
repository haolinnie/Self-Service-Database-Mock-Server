
def test_get_table_name(client):
    res = client.get('/ssd_api/get_table')
    assert res.status_code == 200

def test_get_table(client):
    res = client.get('/ssd_api/get_table/pt_deid')
    assert res.status_code == 200
    res = client.get('/ssd_api/get_table/bla')
    assert res.status_code == 200

def test_get_cols(client):
    res = client.get('/ssd_api/get_table_cols/')
    assert res.status_code == 400
    res = client.get('/ssd_api/get_table_cols/?table_name=pt_deid')
    assert res.status_code == 200
    res = client.get('/ssd_api/get_table_cols/?table_name=bla')
    assert res.status_code == 200

def test_get_distinct(client):
    # Table name required
    res = client.get('/ssd_api/get_distinct/')
    assert res.status_code == 400
    # Success
    res = client.get('/ssd_api/get_distinct/?table_name=pt_deid&col_name=pt_id')
    assert res.status_code == 200
    # Wrong table name
    res = client.get('/ssd_api/get_distinct/?table_name=pt')
    assert res.status_code == 200
    # Correct table name
    res = client.get('/ssd_api/get_distinct/?table_name=pt_deid')
    assert res.status_code == 200
    # Wrong column name
    res = client.get('/ssd_api/get_distinct/?table_name=pt_deid&col_name=bla')
    assert res.status_code == 200
