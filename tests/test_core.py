from api.core import check_sql_safe, create_response, exception_handler


def test_check_sql():
    assert check_sql_safe("12345")
    assert not check_sql_safe("1234;DROP TABLE")
    assert not check_sql_safe("124,123")
    assert not check_sql_safe("123 --bb")


def test_create_response():
    try:
        response = create_response(data="hi")
    except Exception as e:
        assert isinstance(e, TypeError)


def test_exception_handler(app):
    with app.app_context():
        ex = exception_handler(TypeError)
        assert ex[1] == 500
