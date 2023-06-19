from .recognition import VGGFaceRecognizer
from .person import PersonController
face_recognizer = VGGFaceRecognizer(model='senet50')
person_controller = PersonController()
