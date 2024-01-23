from dataclasses import Field
from typing import Dict
from marshmallow import Schema

from marshmallow.fields import Str, Function


def camelcase(s: str) -> str:
    parts = iter(s.split("_"))
    return next(parts) + "".join(i.title() for i in parts)


class CamelCaseSchema(Schema):
    def on_bind_field(self, field_name: str, field_obj: Field):
        field_obj.data_key = camelcase(field_obj.data_key or field_name)


class EmployeeReportSchema(CamelCaseSchema):
    class Meta:
        ordered = True

    def format_amount_paid(obj) -> str:
        return f"${obj.amount_paid}"

    def format_pay_period(obj) -> Dict:
        return {"startDate": obj.start_period, "endDate": obj.end_period}

    employee_id = Str()

    pay_period = Function(format_pay_period)
    amount_paid = Function(format_amount_paid)
