def test_patient_history(client):
    url = "/ssd_api/patients"

    # Empty pt_id does not error
    res = client.get(url)
    assert res.json["success"]

    res = client.get(url + "?pt_id=20676")
    assert res.json["success"]
    assert "20676" in res.json["result"]
    assert "eye_diagnosis" in res.json["result"]["20676"]
    assert "lab_values" in res.json["result"]["20676"]
    assert "medication" in res.json["result"]["20676"]
    assert "pressure" in res.json["result"]["20676"]
    assert "systemic_diagnosis" in res.json["result"]["20676"]
    assert "vision" in res.json["result"]["20676"]


def test_patient_images(client):
    url = "/ssd_api/patient_images"

    # Empty pt_id does not error
    res = client.get(url)
    assert res.json["success"]

    res = client.get(url + "?pt_id=20676")
    assert res.json["success"]
    assert "20676" in res.json["result"]
