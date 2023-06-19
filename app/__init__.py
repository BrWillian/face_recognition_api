from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
import logging

app = FlaskAPI(__name__)
app.config.from_object('config')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("POSTGRESQL_URI")

db = SQLAlchemy(app)
migrate = Migrate(app, db)

LOGGER = logging.getLogger(__name__)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler()
    ]
)

from app.routes import default
from app.models import person