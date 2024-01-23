from typing import Literal
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Query:
    @staticmethod
    def get_payroll_report() -> Literal:
        return """
            with vars as (
                select 15 as mid_month_day
            )
            select
                employee_id,
                case when extract(day from date) > mid_month_day then
                    date_trunc('month', date)::Date + mid_month_day
                else
                    date_trunc('month', date)::Date
                end as start_period,
                case when extract(day from date) > mid_month_day then
                    (date_trunc('month', date) + interval '1 month' - interval '1 day')::Date
                else
                    date_trunc('month', date)::Date + mid_month_day - 1
                end as end_period,
                round(cast(sum(hours_worked) * hourly_pay_rate as numeric), 2) as amount_paid
            from
                vars,
                employee_hours
            inner join
                job_groups
            on
                employee_hours.job_group_id = job_groups.id
            group by
                employee_id, start_period, end_period, hourly_pay_rate
            order by
                employee_id, start_period
            """
