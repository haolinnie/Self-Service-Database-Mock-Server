from api.models._pt_deid import pt_deid
from api.models._diagnosis_deid import diagnosis_deid
from api.models._lab_value_deid import lab_value_deid
from api.models._medication_deid import medication_deid
from api.models._medication_administration_deid import medication_administration_deid
from api.models._smart_data_deid import smart_data_deid
from api.models._visit_movement_deid import visit_movement_deid
from api.models._image_deid import image_deid
from api.models._exam_deid import exam_deid
from api.models._image_procedure import image_procedure
from api.models.User import User
from api.models.base import db


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
