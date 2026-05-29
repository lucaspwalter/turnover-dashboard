from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.employee import Employee
from app.models.turnover_score import TurnoverScore

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


def _latest_score_rows(db: Session):
    latest_scores = (
        db.query(
            TurnoverScore.employee_id,
            func.max(TurnoverScore.id).label("score_id"),
        )
        .group_by(TurnoverScore.employee_id)
        .subquery()
    )

    return (
        db.query(Employee, TurnoverScore)
        .join(TurnoverScore, TurnoverScore.employee_id == Employee.id)
        .join(
            latest_scores,
            (latest_scores.c.employee_id == TurnoverScore.employee_id)
            & (latest_scores.c.score_id == TurnoverScore.id),
        )
        .all()
    )


@router.get("/summary")
def get_dashboard_summary(db: Session = Depends(get_db)):
    rows = _latest_score_rows(db)
    total_employees = len(rows)
    high_risk = sum(1 for _employee, score in rows if score.risk_level == "HIGH")
    medium_risk = sum(1 for _employee, score in rows if score.risk_level == "MEDIUM")
    low_risk = sum(1 for _employee, score in rows if score.risk_level == "LOW")
    total_score = sum(score.score for _employee, score in rows)

    return {
        "total_employees": total_employees,
        "high_risk": high_risk,
        "medium_risk": medium_risk,
        "low_risk": low_risk,
        "high_risk_percentage": (high_risk / total_employees * 100)
        if total_employees
        else 0,
        "average_score": (total_score / total_employees) if total_employees else 0,
    }


@router.get("/by-department")
def get_dashboard_by_department(db: Session = Depends(get_db)):
    departments = {}

    for employee, score in _latest_score_rows(db):
        department = departments.setdefault(
            employee.department,
            {
                "department": employee.department,
                "total_employees": 0,
                "total_score": 0,
                "high_risk": 0,
                "medium_risk": 0,
                "low_risk": 0,
            },
        )

        department["total_employees"] += 1
        department["total_score"] += score.score

        if score.risk_level == "HIGH":
            department["high_risk"] += 1
        elif score.risk_level == "MEDIUM":
            department["medium_risk"] += 1
        elif score.risk_level == "LOW":
            department["low_risk"] += 1

    results = []
    for department in departments.values():
        total_employees = department["total_employees"]
        total_score = department.pop("total_score")
        department["average_score"] = total_score / total_employees
        results.append(department)

    return sorted(results, key=lambda item: item["department"])
