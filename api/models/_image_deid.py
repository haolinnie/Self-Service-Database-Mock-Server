from api.core import Mixin
from api.models.base import db
from api.models._image_procedure import image_procedure


class image_deid(Mixin, db.Model):
    """image_deid table
    """

    __tablename__ = "image_deid"
    image_id = db.Column(db.INT, unique=True, primary_key=True)
    pt_id = db.Column(db.INT, db.ForeignKey("pt_deid.pt_id"))
    image_procedure_id = db.Column(
        db.INT, db.ForeignKey("image_procedure.image_procedure_id")
    )
    exam_id = db.Column(db.INT, db.ForeignKey("exam_deid.exam_id"))

    image_type = db.Column(db.VARCHAR, nullable=False)
    image_laterality = db.Column(db.VARCHAR, nullable=False)
    device_id = db.Column(db.INT)

    @staticmethod
    def get_pt_id_by_image_procedure_type(ipt: list) -> list:
        """Filter pt_id by image_procedure_type

        :param ipt <list<str>> list of image_procedure_type
        :returns <list<int>> pt_id
        """
        # Initialise query
        qry = (
            image_deid.query.with_entities(image_deid.pt_id)
            .distinct()
            .join(image_procedure)
        )

        # construct list of AND queries
        and_query = [
            image_procedure.image_procedure == img_proc_type for img_proc_type in ipt
        ]

        # do the query, get distinct pt_id
        qry = qry.filter(db.and_(*and_query))

        return [v.pt_id for v in qry.all()]
