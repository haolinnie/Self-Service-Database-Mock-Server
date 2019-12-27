from .base import db
from api.core import Mixin


class medication_deid(Mixin, db.Model):
    """medication_deid table
    """

    __tablename__ = "medication_deid"
    medication_id = db.Column(db.INT, unique=True, primary_key=True)
    pt_id = db.Column(db.INT, db.ForeignKey("pt_deid.pt_id"))

    generic_name = db.Column(db.VARCHAR)
    therapeutic_class = db.Column(db.VARCHAR)
    order_placed_dt = db.Column(db.DateTime)
    order_end_dt = db.Column(db.DateTime)
    usage_direction = db.Column(db.VARCHAR)
    order_class = db.Column(db.VARCHAR)
    strength = db.Column(db.VARCHAR)
    form = db.Column(db.VARCHAR)
    number_of_doses = db.Column(db.INT)
    dose_unit = db.Column(db.VARCHAR)
    frequency = db.Column(db.VARCHAR)
