from api.core import Mixin
from api.models.base import db


class image_procedure(Mixin, db.Model):
    """image_procedure table
    """

    __bind_key__ = "image_exams_db"
    __tablename__ = "image_procedure"
    image_procedure_id = db.Column(db.INT, unique=True, primary_key=True)
    image_procedure = db.Column(db.VARCHAR, nullable=False)

    image_deid = db.relationship(
        "image_deid", backref="image_procedure", lazy="dynamic"
    )

    def __repr__(self):
        return "<image_procedure {!r}>".format(self.image_procedure)
