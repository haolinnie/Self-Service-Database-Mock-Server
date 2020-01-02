from datetime import datetime
from .base import db
from ..core import Mixin


class pt_deid(Mixin, db.Model):
    """pt_deid table
    """

    __tablename__ = "pt_deid"
    pt_id = db.Column(db.INT, unique=True, primary_key=True)
    dob = db.Column(db.DateTime, nullable=False)
    over_90 = db.Column(db.SMALLINT)
    ethnicity = db.Column(db.VARCHAR)

    @staticmethod
    def get_all_pt_ids():
        """Get all pt_id available
        """
        qry = pt_deid.query.with_entities(pt_deid.pt_id).distinct()
        return [v.pt_id for v in qry.all()]

        
    @staticmethod
    def get_pt_id_by_age_or_ethnicity(ethnicity: list=None, younger_than: datetime=None, older_than: datetime=None) -> list:
        """Filter pt_id by age and/or ethnicity

        :param ethnicity <list<str>>
        :param younger_than <DateTime> earliest DoB
        :param older_than <DateTime> latest DoB
        :returns <list<int>> pt_id
        """
        
        qry = pt_deid.query.with_entities(pt_deid.pt_id).distinct()

        if younger_than != None :
            qry = qry.filter(
                pt_deid.dob > younger_than
            )
        if older_than != None:
            qry = qry.filter( 
                pt_deid.dob < older_than
            )
        if ethnicity:
            qry = qry.filter(
                pt_deid.ethnicity.in_(ethnicity)
            )

        return [v.pt_id for v in qry.all()]

