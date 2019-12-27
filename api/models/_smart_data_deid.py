from .base import db
from api.core import Mixin


class smart_data_deid(Mixin, db.Model):
    """smart_data_deid table
    """

    __tablename__ = "smart_data_deid"
    smart_data_id = db.Column(db.INT, unique=True, primary_key=True)
    pt_id = db.Column(db.INT, db.ForeignKey("pt_deid.pt_id"))

    element_name = db.Column(db.VARCHAR, nullable=False)
    smrtdta_elem_value = db.Column(db.VARCHAR)
    value_dt = db.Column(db.DateTime)
