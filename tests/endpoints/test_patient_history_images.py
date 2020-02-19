class TestPatientHistory:
    url = "/ssd_api/patients"

    def test_no_id(self, client):
        # Empty pt_id does not error
        res = client.get(self.url)
        assert res.json["success"]

    def test_with_id(self, client):
        res = client.get(self.url + "?pt_id=20676")
        assert "20676" in res.json["result"]
        assert "eye_diagnosis" in res.json["result"]["20676"]
        assert "lab_values" in res.json["result"]["20676"]
        assert "medication" in res.json["result"]["20676"]
        assert "pressure" in res.json["result"]["20676"]
        assert "systemic_diagnosis" in res.json["result"]["20676"]
        assert "vision" in res.json["result"]["20676"]


class TestPatientImages:
    url = "/ssd_api/patient_images"

    def test_no_id(self, client):
        res = client.get(self.url)
        assert res.json["success"]

    def test_with_id(self, client):
        res = client.get(self.url + "?pt_id=20676")
        assert res.json["success"]
        assert "20676" in res.json["result"]
