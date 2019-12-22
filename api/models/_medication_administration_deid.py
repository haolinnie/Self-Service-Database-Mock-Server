from .base import db
from api.core import Mixin


class medication_administration_deid(Mixin, db.Model):
    """medication_administration_deid table
    """

    __tablename__ = "medication_administration_deid"
    medication_administration_id = db.Column(db.INT, unique=True, primary_key=True)
    medication_id = db.Column(db.INT)
    pt_id = db.Column(db.INT)

    generic_name = db.Column(db.VARCHAR)
    therapeutic_class = db.Column(db.VARCHAR)
    order_placed_dt = db.Column(db.DateTime)
    order_end_dt = db.Column(db.DateTime)
    scheduled_administration_dt = db.Column(db.DateTime)
    administration_dt = db.Column(db.DateTime)
    discontinue_order_dt = db.Column(db.DateTime)
    action_name = db.Column(db.VARCHAR)
