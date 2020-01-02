from ._pt_deid import pt_deid
from ._diagnosis_deid import diagnosis_deid
from ._lab_value_deid import lab_value_deid
from ._medication_deid import medication_deid
from ._medication_administration_deid import medication_administration_deid
from ._smart_data_deid import smart_data_deid
from ._visit_movement_deid import visit_movement_deid
from ._image_deid import image_deid
from ._exam_deid import exam_deid
from ._image_procedure import image_procedure
from .base import db


models = {
    "pt_deid": pt_deid,
    "diagnosis_deid": diagnosis_deid,
    "lab_value_deid": lab_value_deid,
    "medication_deid": medication_deid,
    "medication_administration_deid": medication_deid,
    "smart_data_deid": smart_data_deid,
    "visit_movement_deid": visit_movement_deid,
    "image_deid": image_deid,
    "exam_deid": exam_deid,
    "image_procedure": image_procedure,
}


