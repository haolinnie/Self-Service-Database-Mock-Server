from api.auth import verify_password
from api.models.User import User


def test_debug_auth(app_notest):
    with app_notest.app_context():
        assert verify_password("debug", "debug")
        assert not verify_password("fake", "fake")


class TestUser:
    def test_token(self, app_notest, auth_token):
        with app_notest.app_context():
            assert verify_password(auth_token, "nouse")
