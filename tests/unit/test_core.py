import sqlalchemy
from api.models import db, models
from api.core import (
    create_response,
    exception_handler,
    get_database_url,
    get_keywords,
    _generate_like_or_filters,
    _to_list_of_dict,
)


def test_create_response():
    try:
        response = create_response(data="hi")
    except Exception as e:
        assert isinstance(e, TypeError)


def test_exception_handler(app):
    with app.app_context():
        ex = exception_handler(TypeError)
        assert ex[1] == 500


def test_get_database_url():
    res = get_database_url()


def test_get_keywords():
    res = get_keywords()
    assert isinstance(res, dict)


def test_generate_like_or_filters(app):
    with app.app_context():
        res = _generate_like_or_filters(models["pt_deid"].pt_id, ["%[0-9]%"])
        assert isinstance(res, list)
        assert isinstance(res[0], sqlalchemy.sql.elements.BinaryExpression)


def test_to_list_of_dict():
    data = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    res = _to_list_of_dict(data, ["1", "2", "3"])
    assert res[0]["1"] == 1
    assert res[1]["2"] == 5
