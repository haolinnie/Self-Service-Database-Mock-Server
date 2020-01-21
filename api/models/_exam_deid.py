from api.core import Mixin
from api.models.base import db


class exam_deid(Mixin, db.Model):
    """exam_deid table
    """

    __tablename__ = "exam_deid"
    exam_id = db.Column(db.INT, unique=True, primary_key=True)
    pt_id = db.Column(db.INT, db.ForeignKey("pt_deid.pt_id"))

    exam_date = db.Column(db.DateTime)
