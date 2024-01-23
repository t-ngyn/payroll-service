import yaml
from flask import Flask

from database.handler import db
from models import *

DEFAULT_LABEL = "A"
DEFAULT_RATE = 20
JOB_GROUPS_FILE = "job_groups.yaml"


def add_job_groups():
    with open(JOB_GROUPS_FILE, "r") as file:
        data = yaml.safe_load(file)
        for group in data.get("groups", []):
            label, rate = group.get("label", DEFAULT_LABEL), group.get(
                "rate", DEFAULT_RATE
            )

            job_group = JobGroups.get_by_label(label)
            if not job_group:
                JobGroups.create(label=label, hourly_pay_rate=rate)

            print(f"Seeded job group {label}")

        db.session.commit()


def seed_db(app: Flask):
    with app.app_context():
        db.create_all()
        add_job_groups()
