from .base import db
from ..core import Mixin


class image_procedure(Mixin, db.Model):
    """image_procedure table
    """

    __tablename__ = "image_procedure"
    image_procedure_id = db.Column(db.INT, unique=True, primary_key=True)
    image_procedure = db.Column(db.VARCHAR, nullable=False)
