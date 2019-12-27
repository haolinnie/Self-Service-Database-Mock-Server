from .base import db
from api.core import Mixin


class image_deid(Mixin, db.Model):
    """image_deid table
    """

    __tablename__ = "image_deid"
    image_id = db.Column(db.INT, unique=True, primary_key=True)
    pt_id = db.Column(db.INT, db.ForeignKey("pt_deid.pt_id"))
    image_procedure_id = db.Column(
        db.INT, db.ForeignKey("image_procedure.image_procedure_id")
    )
    exam_id = db.Column(db.INT, db.ForeignKey("exam_deid.exam_id"))

    image_type = db.Column(db.VARCHAR, nullable=False)
    image_laterality = db.Column(db.VARCHAR, nullable=False)
    device_id = db.Column(db.INT)
