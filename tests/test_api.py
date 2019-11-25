
def test_get_table_names(client):
    res = client.get('/ssd_api/get_table')
    assert res.status_code == 200


def test_get_cols(client):
    # Test endpoint
    res = client.get('/ssd_api/get_table_cols')
    assert res.status_code == 400
    # Test successful GET
    res = client.get('/ssd_api/get_table_cols?table_name=pt_deid')
    assert res.status_code == 200
    assert "table_name" in res.json
    assert res.json["table_name"] == "pt_deid"
    # Test injection
    res = client.get('/ssd_api/get_table_cols?table_name=some;injection')
    assert res.status_code == 400
    assert "ERROR" in res.json
    # Test wrong table
    res = client.get('/ssd_api/get_table_cols?table_name=bla')
    assert res.status_code == 200
    assert len(res.json['columns']) == 0


def test_get_distinct(client):
    # Table name required
    res = client.get('/ssd_api/get_distinct')
    assert res.status_code == 400
    # Successful GET
    res = client.get('/ssd_api/get_distinct?table_name=pt_deid&col_name=pt_id')
    assert res.status_code == 200
    assert res.json['table_name'] == 'pt_deid'
    # Missing col name
    res = client.get('/ssd_api/get_distinct?table_name=pt_deid')
    assert res.status_code == 400
    # Missing table name
    res = client.get('/ssd_api/get_distinct?col_name=pt_id')
    assert res.status_code == 400
    # Wrong column name
    res = client.get('/ssd_api/get_distinct?table_name=pt_deid&col_name=bla')
    assert res.status_code == 400
    # Test injection
    res = client.get('/ssd_api/get_distinct?table_name=some;injection&col_name=in;a')
    assert res.status_code == 400
    assert "ERROR" in res.json


def test_filter_table_with_ptid(client):
    # Require at least 1 pt_id
    res = client.get('/ssd_api/filter_table_with_ptid') 
    assert res.status_code == 400
    # Must provide table name
    res = client.get('/ssd_api/filter_table_with_ptid?pt_id=100') 
    assert res.status_code == 400
    # Single pt_id query
    res = client.get('/ssd_api/filter_table_with_ptid?pt_id=20676&table_name=pt_deid') 
    assert res.status_code == 200
    assert 'columns' in res.json
    # Multi pt_id query
    res = client.get('/ssd_api/filter_table_with_ptid?pt_id=20676&pt_id=36440&table_name=pt_deid') 
    assert res.status_code == 200
    assert 'columns' in res.json


def test_patient_history(client):
    res = client.get('/ssd_api/patients')
    assert res.status_code == 400
    res = client.get('/ssd_api/patients?pt_id=20676')
    assert res.status_code == 200
    assert '20676' in res.json
    assert 'eye_diagnosis' in res.json['20676']
    assert 'lab_values' in res.json['20676']
    assert 'medication' in res.json['20676']
    assert 'pressure' in res.json['20676']
    assert 'systemic_diagnosis' in res.json['20676']
    assert 'vision' in res.json['20676']


def test_patient_images(client):
    res = client.get('/ssd_api/patient_images')
    assert res.status_code == 400
    res = client.get('/ssd_api/patient_images?pt_id=20676')
    assert res.status_code == 200
    assert '20676' in res.json


def test_Filter_get(client):
    res = client.get('/ssd_api/filter')
    assert res.status_code == 400


def test_Filter_post(client):
    # TODO: Add more tests 
    res = client.post('/ssd_api/filter')
    assert res.status_code == 500

