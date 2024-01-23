import re
from collections import namedtuple
from typing import List, Tuple, Union
from flask import Response, request

from sqlalchemy.sql.expression import text
from sqlalchemy.exc import SQLAlchemyError

from marshmallow.exceptions import ValidationError

from database.handler import db, Query

from models import UploadReportLogs, JobGroups, EmployeeHours
from serializers import EmployeeReportSchema

Columns = namedtuple("Columns", "DATE HOURS_WORKED EMPLOYEE_ID JOB_GROUP")

Column = Columns(0, 1, 2, 3)

ENCODING = "utf-8"


def get_rows(data: str) -> Tuple[List[str], int]:
    # Skip header row
    rows = data.split("\n")[1:]
    total_rows = len(rows)

    return rows, total_rows


def get_row_values(row: str) -> Tuple[str, str, float, str]:
    cells = row.split(",")

    return (
        cells[Column.JOB_GROUP],
        cells[Column.EMPLOYEE_ID],
        float(cells[Column.HOURS_WORKED]),
        cells[Column.DATE],
    )


def get_report_id(filename: str) -> Union[str, None]:
    try:
        pattern = re.compile(r"^time-report-([0-9]+)\.csv$", re.IGNORECASE)
        return pattern.match(filename).group(1)
    except AttributeError:
        return None


class ReportsView:
    def upload_report() -> Response:
        file_data = request.files.get("file")
        filename = file_data.filename

        report_id = get_report_id(filename)
        if report_id == None:
            return (
                "Invalid Filename Format -- Must be of: time-report-[id_number].csv",
                400,
            )

        if UploadReportLogs.has_report_id(report_id):
            return f"Report with ID {report_id} has already been processed", 400

        data = file_data.read().decode(ENCODING)
        rows, total_rows = get_rows(data)
        for row_number, row in enumerate(rows):
            try:
                job_group_label, employee_id, hours_worked, date = get_row_values(row)
            except (ValueError, IndexError):
                return f"Invalid Row (Row Number: {row_number + 1})", 400

            if hours_worked <= 0 or hours_worked > 24:
                return f"Invalid Hours Worked (Row Number: {row_number + 1})", 400

            job_group = JobGroups.get_by_label(job_group_label)
            if not job_group:
                return f"Invalid Job Group (Row Number: {row_number + 1})", 400

            try:
                EmployeeHours.create(
                    job_group_id=job_group.id,
                    employee_id=employee_id,
                    hours_worked=hours_worked,
                    date=date,
                )
            except SQLAlchemyError:
                return f"Failed to process row (Row Number: {row_number + 1})", 400

            print(f"Processed row {row_number + 1}/{total_rows}")

        try:
            UploadReportLogs.create(report_id=report_id)
        except SQLAlchemyError:
            return f"Failed post-processing of report", 500

        db.session.commit()

        return f"Upload Success -- {total_rows} rows processed", 200

    def generate_payroll_report() -> Response:
        try:
            result = db.session.execute(text(Query.get_payroll_report()))

            schema = EmployeeReportSchema()
            report = {
                "payrollReport": {
                    "employeeReports": [schema.dump(row) for row in result.all()]
                }
            }
        except (ValidationError, SQLAlchemyError):
            return f"Failed to generate report", 500

        return report, {"Content-Type": "application/json"}
