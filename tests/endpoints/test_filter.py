class TestFilter:
    url = "/ssd_api/filter"

    def test_get(self, client):
        response = client.get(self.url)
        assert not response.json["success"]
        assert response.status_code == 420

    def test_post(self, client):
        data = {
            "filters": {
                "eye_diagnosis": ["retinal edema"],
                "systemic_diagnosis": ["Sarcoidosis"],
                "age": {"less": 50},
                "ethnicity": [
                    "Not Hispanic or Latino",
                    "Declined",
                    "Hispanic or Latino",
                ],
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
        response = client.post(self.url, json=data)
        assert response.json["success"]
        assert response.content_type == "application/json"

    def test_age(self, client):
        data = {"filters": {"age": {"less": 40}}}
        response = client.post(self.url, json=data)
        assert response.json["result"]["pt_id"] == [59153]

    def test_ethnicity(self, client):
        data = {"filters": {"ethnicity": ["Hispanic or Latino"]}}
        response = client.post(self.url, json=data)
        assert response.json["result"]["pt_id"] == [64153]

    def test_eye_diagnosis(self, client):
        data = {"filters": {"eye_diagnosis": ["retinal edema"]}}
        response = client.post(self.url, json=data)
        assert response.json["result"]["pt_id"] == [36440, 64153]

    def test_systemic_diagnosis(self, client):
        data = {"filters": {"systemic_diagnosis": ["Gout (disorder)"]}}
        response = client.post(self.url, json=data)
        assert response.json["result"]["pt_id"] == [50765]

    def test_images_procedure_type(self, client):
        data = {"filters": {"image_procedure_type": ["IR_OCT"]}}
        response = client.post(self.url, json=data)
        assert response.json["result"]["pt_id"] == [66475, 50765, 36440, 64153, 66172]

    def test_filter_labs(self, client):
        # Test labs : TODO:
        pass

    def test_medication_generic_name(self, client):
        data = {"filters": {"medication_generic_name": ["Ketorolac"]}}
        response = client.post(self.url, json=data)
        assert response.json["success"]
        assert response.json["result"]["pt_id"] == [66475]

    def test_medication_therapeutic_class(self, client):
        data = {"filters": {"medication_therapeutic_class": ["Nutritional Products"]}}
        response = client.post(self.url, json=data)
        assert response.json["success"]
        assert response.json["result"]["pt_id"] == [59153]

    def test_vision(self, client):
        # TODO: Test vision
        pass

    def test_pressure(self, client):
        # Test pressure
        data = {"filters": {"left_pressure": {"less": 10}}}
        response = client.post(self.url, json=data)
        assert response.json["success"]
        assert response.json["result"]["pt_id"] == [64656, 66166]

        data = {"filters": {"left_pressure": {"more": 20}}}
        response = client.post(self.url, json=data)
        assert response.json["success"]
        assert response.json["result"]["pt_id"] == [36440, 66172]

        data = {"filters": {"right_pressure": {"less": 9}}}
        response = client.post(self.url, json=data)
        assert response.json["success"]
        assert response.json["result"]["pt_id"] == [64656]

        data = {"filters": {"right_pressure": {"more": 20}}}
        response = client.post(self.url, json=data)
        assert response.json["success"]
        assert response.json["result"]["pt_id"] == [50765, 64656, 36440, 64153, 66172]
