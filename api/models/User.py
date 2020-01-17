from itsdangerous import 
from api.models.base import db


class User(db.Model):
    """User model for storing login credentials
    """

    __table_name__ = "users"

    id = db.Column(db.Integer, autoincrement=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False)
    admin = db.Column(db.Boolean, nullable=False, default=False)

    def __init__(self, email, password, admin=False):
        self.email = email
        self.password = password
        # TODO: Incomplete
