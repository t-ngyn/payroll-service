from __future__ import annotations

from typing import Union
from uuid import uuid4
from datetime import datetime
from sqlalchemy import (
    Column,
    Integer,
    Date,
    Float,
    String,
    DateTime,
    ForeignKey,
    UniqueConstraint,
)

from sqlalchemy.dialects.postgresql import UUID
from database.handler import db


def get_uuid() -> str:
    return str(uuid4())


def get_datetime() -> datetime:
    return datetime.utcnow()


class JobGroups(db.Model):
    __tablename__ = "job_groups"

    id = Column(UUID(as_uuid=True), primary_key=True, default=get_uuid)
    label = Column(String, nullable=False, unique=True)
    hourly_pay_rate = Column(Float, nullable=False)
    created_at = Column(DateTime, nullable=False, default=get_datetime)
    updated_at = Column(
        DateTime, nullable=False, default=get_datetime, onupdate=get_datetime
    )

    @classmethod
    def get_by_label(cls, label: str):
        return cls.query.with_entities(cls.id).filter(cls.label == label).one_or_none()

    @classmethod
    def create(cls, label: str, hourly_pay_rate: float) -> JobGroups:
        job_group = cls(
            label=label,
            hourly_pay_rate=hourly_pay_rate,
        )

        db.session.add(job_group)

        return job_group


class EmployeeHours(db.Model):
    __tablename__ = "employee_hours"

    __table_args__ = (UniqueConstraint("employee_id", "date"),)

    id = Column(UUID(as_uuid=True), primary_key=True, default=get_uuid)
    employee_id = Column(Integer, nullable=False, index=True)
    job_group_id = Column(ForeignKey("job_groups.id"), nullable=False, index=True)
    date = Column(Date, nullable=False, index=True)
    hours_worked = Column(Float, nullable=False)
    created_at = Column(DateTime, nullable=False, default=get_datetime)
    updated_at = Column(
        DateTime, nullable=False, default=get_datetime, onupdate=get_datetime
    )

    @classmethod
    def create(
        cls,
        job_group_id: str,
        employee_id: int,
        hours_worked: float,
        date: str,
    ) -> EmployeeHours:
        employee_hours = cls(
            job_group_id=job_group_id,
            employee_id=employee_id,
            hours_worked=hours_worked,
            date=datetime.strptime(date, "%d/%m/%Y"),
        )

        db.session.add(employee_hours)

        return employee_hours


class UploadReportLogs(db.Model):
    __tablename__ = "upload_report_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=get_uuid)
    report_id = Column(Integer, nullable=False, index=True)
    created_at = Column(DateTime, nullable=False, default=get_datetime)
    updated_at = Column(
        DateTime, nullable=False, default=get_datetime, onupdate=get_datetime
    )

    @classmethod
    def has_report_id(cls, report_id: Union[str, int]) -> bool:
        return bool(
            cls.query.with_entities(cls.report_id)
            .filter(cls.report_id == report_id)
            .first()
        )

    @classmethod
    def create(
        cls,
        report_id: int,
    ) -> UploadReportLogs:
        upload_log = cls(report_id=report_id)

        db.session.add(upload_log)

        return upload_log
