from .base import db
from api.core import Mixin, KEYWORDS


class smart_data_deid(Mixin, db.Model):
    """smart_data_deid table
    """

    __tablename__ = "smart_data_deid"
    smart_data_id = db.Column(db.INT, unique=True, primary_key=True)
    pt_id = db.Column(db.INT, db.ForeignKey("pt_deid.pt_id"))

    element_name = db.Column(db.VARCHAR, nullable=False)
    smrtdta_elem_value = db.Column(db.VARCHAR)
    value_dt = db.Column(db.DateTime)

    @staticmethod
    def get_pt_id_by_vision_pressure(left_vision_less=None,
                                     left_vision_more=None,
                                     right_vision_less=None,
                                     right_vision_more=None,
                                     left_pressure_less=None,
                                     left_pressure_more=None,
                                     right_pressure_less=None,
                                     right_pressure_more=None
                                     ):
        """Get pt_id by vision

        :param
        :returns
        """
        # Initialise query
        qry = smart_data_deid.query.with_entities(smart_data_deid.pt_id).distinct()

        # Do query
        if left_vision_less != None or left_vision_more != None:
            and_query = [
                smart_data_deid.element_name.ilike(KEYWORDS["left_vision"])
            ]
            if left_vision_less != None:
                and_query.append(
                    smart_data_deid.smrtdta_elem_value
                    >= left_vision_less
                )
            if left_vision_more != None:
                and_query.append(
                    smart_data_deid.smrtdta_elem_value
                    <= left_vision_more
                )
            qry = qry.filter(db.and_(*and_query))

        if right_vision_less != None or right_vision_more != None:
            and_query = [
                smart_data_deid.element_name.ilike(KEYWORDS["right_vision"])
            ]
            if right_vision_less != None:
                and_query.append(
                    smart_data_deid.smrtdta_elem_value
                    >= right_vision_less
                )
            if right_vision_more != None:
                and_query.append(
                    smart_data_deid.smrtdta_elem_value
                    <= right_vision_more
                )
            qry = qry.filter(db.and_(*and_query))

        if left_pressure_less != None or left_pressure_more != None:
            and_query = [
                smart_data_deid.element_name.ilike(KEYWORDS["left_pressure"])
            ]
            if left_pressure_less != None:
                and_query.append(
                    smart_data_deid.smrtdta_elem_value
                    <= left_pressure_less
                )
            if left_pressure_more != None:
                and_query.append(
                    smart_data_deid.smrtdta_elem_value
                    >= left_pressure_more
                )
            qry = qry.filter(db.and_(*and_query))

        if right_pressure_less != None or right_pressure_more != None:
            and_query = [
                smart_data_deid.element_name.ilike(KEYWORDS["right_pressure"])
            ]
            if right_pressure_less != None:
                and_query.append(
                    smart_data_deid.smrtdta_elem_value
                    <= right_pressure_less
                )
            if right_pressure_more != None:
                and_query.append(
                    smart_data_deid.smrtdta_elem_value
                    >= right_pressure_more
                )
            qry = qry.filter(db.and_(*and_query))
            
        return [v.pt_id for v in qry.all()]


