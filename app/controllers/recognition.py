from keras_vggface.utils import preprocess_input
from keras_vggface.vggface import VGGFace
from scipy.spatial.distance import cosine
from app.models.person import Person
from PIL import Image
from mtcnn import MTCNN
import numpy as np
import pickle
import time


class VGGFaceRecognizer:
    def __init__(self, model='senet50'):
        self.model = model
        self.face_dict = dict()
        self.recognizer = VGGFace(include_top=False, model=model)
        self.mtcnn = MTCNN()

    @staticmethod
    def calculate_similarity(vector_1, vector_2):
        vector_1 = np.squeeze(vector_1)
        vector_2 = np.squeeze(vector_2)

        return cosine(vector_1, vector_2)

    def get_face(self, image: np.ndarray):

        detected_faces = self.mtcnn.detect_faces(image)

        height, width, _ = image.shape

        if not detected_faces:
            return None

        face = max(detected_faces, key=lambda detected_face: detected_face['confidence'])
        x1, y1, x2, y2 = VGGFaceRecognizer.fix_coordinates(face['box'], width, height)
        cropped_face = image[y1:y2, x1:x2]

        cropped_face = Image.fromarray(cropped_face)

        return cropped_face

    def feature_extractor(self, face):
        face = face.resize((224, 224), Image.ANTIALIAS)
        face = np.asarray(face).astype(np.float64)
        face = np.expand_dims(face, axis=0)

        face = preprocess_input(face, version=2)

        return self.recognizer.predict(face)

    def recognize(self, image: np.ndarray) -> dict:
        start_time = time.time()
        cropped_face = self.get_face(image)

        if not cropped_face:
            return {"face_id": None, "face_score": None, "inference_time": round(time.time() - start_time, 4)}

        db_faces = Person.query.all()

        list_of_faces = {face.code: pickle.loads(face.face_attributes) for face in db_faces}

        face_dict = self.find_face(
            cropped_face, list_of_faces, thresh=0.35)

        end_time = time.time() - start_time
        face_dict["inferece_time"] = round(end_time, 4)

        person = (next((person for person in db_faces if person.code == 3), None))

        face_dict["name"] = person.name
        face_dict["sex"] = person.sex
        face_dict["phone"] = person.phone
        face_dict["email"] = person.email

        return face_dict

    def find_face(self, face: np.ndarray, list_of_faces: dict, thresh: float = 0.25) -> dict:
        query_features = self.feature_extractor(face)
        temp_sim_dict = dict()

        for key, value in list_of_faces.items():
            if isinstance(value, np.ndarray):
                db_face_features = np.array(value)

                score = self.calculate_similarity(
                    db_face_features.squeeze(), query_features.flatten()
                )
                temp_sim_dict[key] = score
        return {"face_id": 0, "face_score": 0.0} if min(temp_sim_dict.values()) > thresh else {
            "face_id": min(temp_sim_dict, key=temp_sim_dict.get), "face_score": min(temp_sim_dict.values())}

    @staticmethod
    def fix_coordinates(box: list, width: int, height: int):
        x1, y1, w, h = box
        x1 = max(x1, 0)
        y1 = max(y1, 0)
        x2 = min(w, width) + x1
        y2 = min(h, height) + y1
        return x1, y1, x2, y2
