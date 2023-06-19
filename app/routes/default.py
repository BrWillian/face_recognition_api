from flask import request, make_response, Response
from flask import jsonify
from app import LOGGER
from app.controllers import face_recognizer
from app.controllers import person_controller
import cv2
import base64
import numpy as np
from app import app


@app.route('/api/face/recognizer', methods=['POST'])
def recognizer():
    if request.method == "POST":
        try:
            imgb64 = request.data['image']
            image = np.fromstring(base64.b64decode(imgb64), np.uint8)
            image = cv2.imdecode(image, cv2.IMREAD_COLOR)

            face_dict = face_recognizer.recognize(image)
            LOGGER.info(face_dict)

            return make_response(jsonify(face_dict), 200) if face_dict['face_id'] else Response(
                status=404)
        except Exception as e:
            LOGGER.error(e)
            return Response(status=500)


@app.route('/api/face/register', methods=['POST'])
def add_face():
    if request.method == "POST":
        try:
            imgb64 = request.data['image']
            name = request.data['name']
            sex = request.data['sex'] if request.data['sex'] else None
            phone = request.data['phone'] if request.data['phone'] else None
            email = request.data['email'] if request.data['email'] else None
            image = np.fromstring(base64.b64decode(imgb64), np.uint8)
            image = cv2.imdecode(image, cv2.IMREAD_COLOR)

            cropped_face = face_recognizer.get_face(image)

            features = face_recognizer.feature_extractor(cropped_face)

            person = {
                "name": name,
                "sex": sex,
                "phone": phone,
                "email": email,
                "image": imgb64,
                "face_attributes": np.array(features.squeeze())
            }

            if person_controller.create(person):
                return Response(status=201)

            return Response(status=400)

        except Exception as e:
            LOGGER.error(e)
            return Response(status=500)
