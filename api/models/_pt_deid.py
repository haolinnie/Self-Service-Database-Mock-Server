from .base import db
from api.core import Mixin


class pt_deid(Mixin, db.Model):
    """pt_deid table
    """

    __tablename__ = "pt_deid"
    pt_id = db.Column(db.INT, unique=True, primary_key=True)
    dob = db.Column(db.DateTime, nullable=False)
    over_90 = db.Column(db.SMALLINT)
    ethnicity = db.Column(db.VARCHAR)
