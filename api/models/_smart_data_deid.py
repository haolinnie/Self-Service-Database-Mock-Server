from api.core import Mixin, KEYWORDS
from api.models.base import db


def _vision_filter(lst, more_than, less_than):
    """Helper function that takes a list of tuples<pt_id, val>
    filter for val between more_than and less_than for vision
    
    """
    more_than = 0 if more_than is None else more_than
    less_than = 1000 if less_than is None else less_than
    return [
        (pt_id, val)
        for pt_id, val in lst
        if more_than <= int(val.split("/")[1].split("-")[0].split("+")[0]) <= less_than
    ]


def _pressure_filter(lst, more_than, less_than):
    """Helper function that takes a list of tuples<pt_id, val>
    filter for val between more_than and less_than for pressure
    """
    more_than = 0 if more_than is None else more_than
    less_than = 1000 if less_than is None else less_than
    return [(pt_id, val) for pt_id, val in lst if more_than <= int(val) <= less_than]


def _filter_vis_pres_range(
    elem_keywords, value_range, value_validation_regex, vision=False
):
    qry = smart_data_deid.query.with_entities(
        smart_data_deid.pt_id, smart_data_deid.smrtdta_elem_value
    )
    qry = qry.filter(
        db.and_(
            smart_data_deid.element_name.ilike(elem_keywords),
            smart_data_deid.smrtdta_elem_value.ilike(value_validation_regex),
        )
    )
    pt_ids = qry.all()

    if vision:
        pt_ids = list(set(v[0] for v in _vision_filter(pt_ids, *value_range)))
    else:  # Pressure
        pt_ids = list(set(v[0] for v in _pressure_filter(pt_ids, *value_range)))

    return pt_ids


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
    def get_pt_id_by_left_vision(val_range):
        return _filter_vis_pres_range(
            KEYWORDS["left_vision"],
            val_range,
            KEYWORDS["vision_value_regex"],
            vision=True,
        )

    @staticmethod
    def get_pt_id_by_right_vision(val_range):
        return _filter_vis_pres_range(
            KEYWORDS["right_vision"],
            val_range,
            KEYWORDS["vision_value_regex"],
            vision=True,
        )

    @staticmethod
    def get_pt_id_by_left_pressure(val_range):
        return _filter_vis_pres_range(
            KEYWORDS["left_pressure"],
            val_range,
            KEYWORDS["pressure_value_regex"],
            vision=False,
        )

    @staticmethod
    def get_pt_id_by_right_pressure(val_range):
        return _filter_vis_pres_range(
            KEYWORDS["right_pressure"],
            val_range,
            KEYWORDS["pressure_value_regex"],
            vision=False,
        )

    @staticmethod
    def get_data_for_pt_id(pt_id, pressure=False, vision=False):
        if not pressure ^ vision:
            raise ValueError(
                "get_data_for_pt_id: set either pressure or vision to True"
            )

        if pressure:
            kws = KEYWORDS["pressure"]
        elif vision:
            kws = KEYWORDS["vision"]

        qry = (
            smart_data_deid.query.with_entities(
                smart_data_deid.element_name,
                smart_data_deid.smrtdta_elem_value,
                smart_data_deid.smart_data_id,
                smart_data_deid.value_dt,
            )
            .filter(
                db.and_(
                    smart_data_deid.pt_id == curr_id,
                    smart_data_deid.element_name.ilike(kws),
                )
            )
            .order_by(smart_data_deid.value_dt.desc())
        )
        res = qry.all()
        return res
