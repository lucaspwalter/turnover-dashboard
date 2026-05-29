from datetime import date

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.employee import Employee
from app.models.employee_event import EmployeeEvent
from app.models.turnover_score import TurnoverScore


PROMOTION_POINTS = 20
BELOW_ROLE_AVERAGE_SALARY_POINTS = 20
ABSENCES_POINTS = 15
SHORT_TENURE_POINTS = 15
WARNINGS_POINTS = 15
NO_RAISE_POINTS = 15


def _years_ago(years: int) -> date:
    today = date.today()
    try:
        return today.replace(year=today.year - years)
    except ValueError:
        return today.replace(month=2, day=28, year=today.year - years)


def calculate_score(db: Session, employee_id: int):
    employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if not employee:
        return None

    today = date.today()
    one_year_ago = _years_ago(1)
    two_years_ago = _years_ago(2)

    factors = {
        "no_promotion_over_2_years": 0,
        "salary_below_role_average": 0,
        "absences_over_3_last_12_months": 0,
        "tenure_under_1_year": 0,
        "warnings_last_12_months": 0,
        "no_raise_last_12_months": 0,
    }

    latest_promotion = (
        db.query(func.max(EmployeeEvent.event_date))
        .filter(
            EmployeeEvent.employee_id == employee.id,
            EmployeeEvent.event_type == "PROMOTION",
        )
        .scalar()
    )
    promotion_reference_date = latest_promotion or employee.hire_date
    if promotion_reference_date < two_years_ago:
        factors["no_promotion_over_2_years"] = PROMOTION_POINTS

    role_average_salary = (
        db.query(func.avg(Employee.salary))
        .filter(Employee.role == employee.role)
        .scalar()
    )
    if role_average_salary is not None and employee.salary < role_average_salary:
        factors["salary_below_role_average"] = BELOW_ROLE_AVERAGE_SALARY_POINTS

    absences_last_12_months = (
        db.query(func.count(EmployeeEvent.id))
        .filter(
            EmployeeEvent.employee_id == employee.id,
            EmployeeEvent.event_type == "ABSENCE",
            EmployeeEvent.event_date >= one_year_ago,
            EmployeeEvent.event_date <= today,
        )
        .scalar()
    )
    if absences_last_12_months > 3:
        factors["absences_over_3_last_12_months"] = ABSENCES_POINTS

    if employee.hire_date > one_year_ago:
        factors["tenure_under_1_year"] = SHORT_TENURE_POINTS

    warnings_last_12_months = (
        db.query(func.count(EmployeeEvent.id))
        .filter(
            EmployeeEvent.employee_id == employee.id,
            EmployeeEvent.event_type == "WARNING",
            EmployeeEvent.event_date >= one_year_ago,
            EmployeeEvent.event_date <= today,
        )
        .scalar()
    )
    if warnings_last_12_months > 0:
        factors["warnings_last_12_months"] = WARNINGS_POINTS

    latest_raise = (
        db.query(func.max(EmployeeEvent.event_date))
        .filter(
            EmployeeEvent.employee_id == employee.id,
            EmployeeEvent.event_type == "RAISE",
        )
        .scalar()
    )
    raise_reference_date = latest_raise or employee.hire_date
    if raise_reference_date < one_year_ago:
        factors["no_raise_last_12_months"] = NO_RAISE_POINTS

    score = min(sum(factors.values()), 100)
    risk_level = _risk_level(score)

    turnover_score = TurnoverScore(
        employee_id=employee.id,
        score=score,
        risk_level=risk_level,
    )
    db.add(turnover_score)
    db.commit()
    db.refresh(turnover_score)

    return {
        "score": score,
        "risk_level": risk_level,
        "factors": factors,
    }


def recalculate_all(db: Session):
    employees = db.query(Employee).all()
    return [
        {
            "employee_id": employee.id,
            **calculate_score(db, employee.id),
        }
        for employee in employees
    ]


def _risk_level(score: int):
    if score < 40:
        return "LOW"
    if score <= 70:
        return "MEDIUM"
    return "HIGH"
