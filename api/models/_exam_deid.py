from api.core import Mixin
from api.models.base import db


class exam_deid(Mixin, db.Model):
    """exam_deid table
    """

    __bind_key__ = "image_exams_db"
    __tablename__ = "exam_deid"
    exam_id = db.Column(db.INT, unique=True, primary_key=True)
    pt_id = db.Column(db.INT, db.ForeignKey("pt_deid.pt_id"))

    exam_date = db.Column(db.DateTime)

    image_deid = db.relationship("image_deid", backref="exam_deid", lazy="dynamic")

    def __repr__(self):
        return "<exam_deid {!r}, pt_id {!r}>".format(self.exam_id, self.pt_id)
