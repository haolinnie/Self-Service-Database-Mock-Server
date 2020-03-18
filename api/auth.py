from flask import g, current_app
from flask_httpauth import HTTPBasicAuth

from api.models.User import User


auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(username_or_token, password):
    if current_app.config.get("TESTING"):
        return True

    user = User.verify_auth_token(username_or_token)

    if not user:
        user = User.query.filter_by(username=username_or_token).first()
        if not user or not user.verify_password(password):
            return False
    g.user = user
    return True
