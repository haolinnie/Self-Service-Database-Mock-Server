from .base import db
from api.core import Mixin


class image_deid(Mixin, db.Model):
    """image_deid table
    """

    __tablename__ = "image_deid"
    image_id = db.Column(db.INT, unique=True, primary_key=True)
    pt_id = db.Column(db.INT)

    image_type = db.Column(db.VARCHAR, nullable=False)
    image_laterality = db.Column(db.VARCHAR, nullable=False)
    exam_id = db.Column(db.INT)
    device_id = db.Column(db.INT)
    image_procedure_id = db.Column(db.INT)
