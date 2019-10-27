
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
    assert res.status_code == 200
    res = client.get('/ssd_api/get_table_cols/?table_name=pt_deid')
    assert res.status_code == 200
    res = client.get('/ssd_api/get_table_cols/?table_name=bla')
    assert res.status_code == 200

def test_get_distinct(client):
    # Table name required
    res = client.get('/ssd_api/get_distinct/')
    assert res.status_code == 200
    # Success
    res = client.get('/ssd_api/get_distinct/?table_name=pt_deid&col_name=pt_id')
    assert res.status_code == 200
    # Missing col name
    res = client.get('/ssd_api/get_distinct/?table_name=pt_deid')
    assert res.status_code == 200
    # Wrong column name
    res = client.get('/ssd_api/get_distinct/?table_name=pt_deid&col_name=bla')
    assert res.status_code == 200

def test_filter_table_with_ptid(client):
    # Require at least 1 pt_id
    res = client.get('/ssd_api/filter_table_with_ptid/') 
    assert res.status_code == 200
    # Must provide table name
    res = client.get('/ssd_api/filter_table_with_ptid/?pt_id=100') 
    assert res.status_code == 200
    # Single pt_id query
    res = client.get('/ssd_api/filter_table_with_ptid/?pt_id=20676&table_name=pt_deid') 
    assert res.status_code == 200
    # Multi pt_id query
    res = client.get('/ssd_api/filter_table_with_ptid/?pt_id=20676&pt_id=36440&table_name=pt_deid') 
    assert res.status_code == 200
