import pytest
from api.models import db, models

def test_pt_deid(app):
    with app.app_context():
        
        res = models["pt_deid"].get_all_pt_ids()
        assert isinstance(res, list)


# def test_get_table_columns(app):
    # with app.app_context():
        # res = db_utils.get_table_columns("pt_deid")
    # assert res is not None
