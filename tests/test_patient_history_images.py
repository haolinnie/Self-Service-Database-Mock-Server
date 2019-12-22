def test_patient_history(client):
    # Empty pt_id does not error
    res = client.get("/ssd_api/patients")
    assert res.json["success"] == True

    res = client.get("/ssd_api/patients?pt_id=20676")
    assert res.json["success"]
    assert "20676" in res.json["result"]
    assert "eye_diagnosis" in res.json["result"]["20676"]
    assert "lab_values" in res.json["result"]["20676"]
    assert "medication" in res.json["result"]["20676"]
    assert "pressure" in res.json["result"]["20676"]
    assert "systemic_diagnosis" in res.json["result"]["20676"]
    assert "vision" in res.json["result"]["20676"]


def test_patient_images(client):
    # Empty pt_id does not error
    res = client.get("/ssd_api/patient_images")
    assert res.json["success"] == True

    res = client.get("/ssd_api/patient_images?pt_id=20676")
    assert res.json["success"]
    assert "20676" in res.json["result"]
