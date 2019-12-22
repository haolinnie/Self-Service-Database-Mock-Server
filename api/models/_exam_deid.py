from .base import db
from api.core import Mixin


class exam_deid(Mixin, db.Model):
    """exam_deid table
    """

    __tablename__ = "exam_deid"
    exam_id = db.Column(db.INT, unique=True, primary_key=True)
    pt_id = db.Column(db.INT)

    exam_date = db.Column(db.DateTime)
