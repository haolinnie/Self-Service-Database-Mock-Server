from api.core import Mixin
from api.models.base import db


class lab_value_deid(Mixin, db.Model):
    """lab_value_deid table
    """

    __tablename__ = "lab_value_deid"
    lab_value_id = db.Column(db.INT, unique=True, primary_key=True)
    pt_id = db.Column(db.INT, db.ForeignKey("pt_deid.pt_id"))

    name = db.Column(db.VARCHAR, nullable=False)
    loinc_code = db.Column(db.VARCHAR)
    value = db.Column(db.VARCHAR)
    reference_high = db.Column(db.VARCHAR)
    reference_low = db.Column(db.VARCHAR)
    reference_normal = db.Column(db.VARCHAR)
    reference_unit = db.Column(db.VARCHAR)
    result_category = db.Column(db.VARCHAR)
    order_dt = db.Column(db.DateTime)
    result_dt = db.Column(db.DateTime)
    value_numeric = db.Column(db.DECIMAL(18, 0))
