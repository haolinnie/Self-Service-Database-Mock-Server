from api.core import Mixin
from api.models.base import db


class medication_administration_deid(Mixin, db.Model):
    """medication_administration_deid table
    """

    __tablename__ = "medication_administration_deid"
    medication_administration_id = db.Column(db.INT, unique=True, primary_key=True)
    medication_id = db.Column(db.INT, db.ForeignKey("medication_deid.medication_id"))
    pt_id = db.Column(db.INT, db.ForeignKey("pt_deid.pt_id"))

    generic_name = db.Column(db.VARCHAR)
    therapeutic_class = db.Column(db.VARCHAR)
    order_placed_dt = db.Column(db.DateTime)
    order_end_dt = db.Column(db.DateTime)
    scheduled_administration_dt = db.Column(db.DateTime)
    administration_dt = db.Column(db.DateTime)
    discontinue_order_dt = db.Column(db.DateTime)
    action_name = db.Column(db.VARCHAR)

    def __repr__(self):
        return "<medication_administration_deid {!r}, pt_id {!r}".format(
            self.medication_administration_id, self.pt_id
        )
