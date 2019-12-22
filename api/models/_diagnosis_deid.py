from .base import db
from api.core import Mixin


class diagnosis_deid(Mixin, db.Model):
    """diagnosis_deid table
    """

    __tablename__ = "diagnosis_deid"
    diagnosis_id = db.Column(db.INT, unique=True, primary_key=True)
    pt_id = db.Column(db.INT)

    diagnosis_name = db.Column(db.VARCHAR)
    diagnosis_code = db.Column(db.VARCHAR, nullable=False)
    diagnosis_code_set = db.Column(db.VARCHAR)
    diagnosis_start_dt = db.Column(db.DateTime)
    diagnosis_end_dt = db.Column(db.DateTime)
