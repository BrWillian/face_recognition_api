from sqlalchemy import Column, Integer, String, Boolean, Text, DateTime
import pickle as pkl
from app import db
from datetime import datetime


class Person(db.Model):
    __tablename__ = "person"
    __table_args__ = {'extend_existing': True}
    code = Column("code", Integer, primary_key=True, autoincrement=True)
    name = Column("name", String)
    sex = Column("sex", String, nullable=True, default=None)
    phone = Column("phone", String, nullable=True, default=None)
    email = Column("email", String, nullable=True, default=None)
    image = Column("image", Text)
    face_attributes = Column("face_attributes", db.PickleType)
    dt_created = Column("dt_created", DateTime)
    dt_updated = Column("dt_updated", DateTime)

    def __init__(self, name, sex, phone, email, image, face_attributes):
        self.name = name
        self.sex = sex
        self.phone = phone
        self.email = email
        self.image = image
        self.face_attributes = pkl.dumps(face_attributes)
        self.dt_created = datetime.now()
        self.dt_updated = datetime.now()
