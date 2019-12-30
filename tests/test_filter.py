def test_filter_get(client):
    url = "/ssd_api/filter"
    response = client.get(url)
    assert not response.json["success"]
    assert response.status_code == 420


def test_filter_post(client):
    url = "/ssd_api/filter"
    # TODO: Add more tests

    data = {
        "filters": {
            "eye_diagnosis": ["retinal edema"],
            "systemic_diagnosis": ["Sarcoidosis"],
            "age": {"less": 50},
            "ethnicity": ["Not Hispanic or Latino", "Declined", "Hispanic or Latino"],
            "image_procedure_type": ["IR_OCT"],
            "labs": {"Calcium": 4},
            "medication_generic_name": ["Ketorolac"],
            "medication_therapuetic_name": ["CNS Agent"],
            "left_vision": {"less": "20/40"},
            "right_vision": {"less": "20/40", "more": "20/200"},
            "left_pressure": {"less": 50},
            "right_pressure": {"equal": 100, "between": [120, 200]},
        }
    }
    response = client.post(url, json=data)
    assert response.json["success"]
    assert response.content_type == "application/json"

    # Test age
    data = { "filters": { "age" : {"less": 40} } }
    response = client.post(url, json=data)
    assert response.json["success"]
    assert response.json["result"]["pt_id"] == [59153]

    # Test ethnicity
    data = { "filters": { "ethnicity" : ["Hispanic or Latino"] } }
    response = client.post(url, json=data)
    assert response.json["success"]
    assert response.json["result"]["pt_id"] == [64153]

    # Test eye_diagnosis
    data = {"filters": {"eye_diagnosis": ["retinal edema"]}}
    response = client.post(url, json=data)
    assert response.json["success"]
    assert response.json["result"]["pt_id"] == [36440, 64153]

    # Test systemic_diagnosis
    data = {"filters": {"systemic_diagnosis": ["Gout (disorder)"]}}
    response = client.post(url, json=data)
    assert response.json["success"]
    assert response.json["result"]["pt_id"] == [50765]

    # Test image_procedure_type
    data = { "filters": { "image_procedure_type": ["IR_OCT"] } }
    response = client.post(url, json=data)
    assert response.json["success"]
    assert response.json["result"]["pt_id"] == [66475, 50765, 36440, 64153, 66172]

    # Test labs : TODO:

    # Test medication_generic_name
    data = { "filters": { "medication_generic_name": ["Ketorolac"] } }
    response = client.post(url, json=data)
    assert response.json["success"]
    assert response.json["result"]["pt_id"] == [66475]

    # Test medication_therapeutic_class 
    data = { "filters": { "medication_therapeutic_class": ["Nutritional Products"] } }
    response = client.post(url, json=data)
    assert response.json["success"]
    assert response.json["result"]["pt_id"] == [59153]


    # TODO: Test vision

    # TODO: Test pressure


