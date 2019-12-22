def test_filter_get(client):
    response = client.get("/ssd_api/filter")
    assert response.json["success"] == False
    assert response.status_code == 500


def test_filter_post(client):
    # TODO: Add more tests
    url = "/ssd_api/filter"
    data = {
        "filters": {
            "eye_diagnosis": ["retinal edema"],
            "systemic_diagnosis": ["gout"],
            "age": {"less": 50},
            "ethnicity": ["asian"],
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
