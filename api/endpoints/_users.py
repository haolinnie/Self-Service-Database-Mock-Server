from flask import Blueprint, request, g, jsonify

from api.models import db, User
from api.core import create_response
from api.auth import auth


_users = Blueprint("_users", __name__)


@_users.route("/ssd_api/users", methods=["get"])
@auth.login_required
def get_users():
    """ GET: List users
    """
    users = User.query.with_entities(User.username).all()
    return create_response(data={"users": [user[0] for user in users]})


@_users.route("/ssd_api/users", methods=["post"])
def new_user():
    """ POST: Create a new user
    """
    username = request.json.get("username")
    password = request.json.get("password")
    if username is None or password is None:
        return create_response(message="Missing arguments", status=420)
    # Check if user exists
    temp = User.query.filter_by(username=username).first()
    if temp:
        return create_response(message="User '{}' exists".format(username), status=420)

    user = User(username=username)
    user.hash_password(password)
    db.session.add(user)
    db.session.commit()
    return create_response(message="Created user", data={"username": format(username)})


@_users.route("/ssd_api/users", methods=["delete"])
@auth.login_required
def delete_user():
    """ DELETE: Delete a user
    """
    username = g.user.username
    db.session.delete(g.user)
    db.session.commit()
    return create_response(message="Delete", data={"username": format(username)})


@_users.route("/ssd_api/token", methods=["get"])
@auth.login_required
def get_auth_token():
    """ Generate an authorization token
    
    Sending the username and password with every request
    is dangerous even with the encryptions of a post request.
    
    A temporary token is therefore preferred.
    """
    token = g.user.generate_auth_token()

    return create_response(data={"token": token.decode("ascii")})


@_users.route("/ssd_api/whoami", methods=["get"])
@auth.login_required
def resource():
    return create_response(message="Hello {}".format(g.user.username))
