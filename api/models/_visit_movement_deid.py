from .base import db
from ..core import Mixin


class visit_movement_deid(Mixin, db.Model):
    """visit_movement_deid table
    """

    __tablename__ = "visit_movement_deid"
    visit_movement_id = db.Column(db.INT, unique=True, primary_key=True)
    pt_id = db.Column(db.INT, db.ForeignKey("pt_deid.pt_id"))

    department_external_name = db.Column(db.VARCHAR)
    department_name = db.Column(db.VARCHAR, nullable=False)
    event_start_dt = db.Column(db.DateTime)
    event_end_dt = db.Column(db.DateTime)
    event_type_name = db.Column(db.VARCHAR)
    event_subtype_name = db.Column(db.VARCHAR)
    patient_class_name = db.Column(db.VARCHAR)
