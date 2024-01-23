import os
from connexion import FlaskApp
from dotenv import load_dotenv
from database.handler import db
from database.seed import seed_db

load_dotenv()

application = FlaskApp(__name__, specification_dir="./openapi")
application.app.json.sort_keys = False
application.app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("SQLALCHEMY_DATABASE_URI")

print("Initializing Database")
db.init_app(application.app)
seed_db(application.app)

print("Setting up API")
application.add_api("reports.yaml")
