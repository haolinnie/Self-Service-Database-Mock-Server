import pytest
from api.models import db, models


def test_pt_deid(app):
    with app.app_context():

        res = models["pt_deid"].get_all_pt_ids()
        assert isinstance(res, list)
