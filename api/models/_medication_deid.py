from sqlalchemy import func

from api.core import Mixin
from api.models.base import db


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
    usage_directions = db.Column(db.VARCHAR)
    order_class = db.Column(db.VARCHAR)
    strength = db.Column(db.VARCHAR)
    form = db.Column(db.VARCHAR)
    number_of_doses = db.Column(db.INT)
    dose_unit = db.Column(db.VARCHAR)
    frequency = db.Column(db.VARCHAR)

    medication_administration_deid = db.relationship(
        "medication_administration_deid", backref="medication_deid", lazy="dynamic"
    )

    def __repr__(self):
        return "<medication_deid {!r}, pt_id {!r}".format(
            self.medication_id, self.pt_id
        )

    @staticmethod
    def get_pt_id_by_generic_name(mgn: list) -> list:
        """Get pt_id by medication_generic_name
        
        :param mgn <list<str>> list of medication_generic_name
        :returns <list<int>> list of pt_id
        """
        # Initialise query
        qry = medication_deid.query.with_entities(medication_deid.pt_id).distinct()

        # do query
        qry = qry.filter(
            func.lower(medication_deid.generic_name).in_([v.lower() for v in mgn])
        )

        return [v.pt_id for v in qry.all()]

    @staticmethod
    def get_pt_id_by_therapeutic_class(mtc: list) -> list:
        """Get pt_id by medication_generic_name
        
        :param mgn <list<str>> list of medication_generic_name
        :returns <list<int>> list of pt_id
        """
        # Initialise query
        qry = medication_deid.query.with_entities(medication_deid.pt_id).distinct()

        # do query
        qry = qry.filter(
            func.lower(medication_deid.therapeutic_class).in_([v.lower() for v in mtc])
        )

        return [v.pt_id for v in qry.all()]
