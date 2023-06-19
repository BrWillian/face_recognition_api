from app.models.person import Person
from app import LOGGER
from app import db


class PersonController:
    @staticmethod
    def create(person: dict) -> bool:
        try:
            person = Person(
                name=person["name"],
                sex=person["sex"],
                phone=person["phone"],
                email=person["email"],
                image=person["image"],
                face_attributes=person["face_attributes"]
            )

            db.session.add(person)
            db.session.commit()

            return True
        except Exception as e:
            LOGGER.error(e)
            return False