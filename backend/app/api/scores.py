from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.employee import Employee
from app.models.turnover_score import TurnoverScore
from app.services import score_service

router = APIRouter(prefix="/scores", tags=["scores"])


@router.post("/recalculate")
def recalculate_scores(db: Session = Depends(get_db)):
    return score_service.recalculate_all(db)


@router.get("/ranking")
def get_ranking(db: Session = Depends(get_db)):
    latest_scores = (
        db.query(
            TurnoverScore.employee_id,
            func.max(TurnoverScore.id).label("score_id"),
        )
        .group_by(TurnoverScore.employee_id)
        .subquery()
    )

    rows = (
        db.query(Employee, TurnoverScore)
        .join(TurnoverScore, TurnoverScore.employee_id == Employee.id)
        .join(
            latest_scores,
            (latest_scores.c.employee_id == TurnoverScore.employee_id)
            & (latest_scores.c.score_id == TurnoverScore.id),
        )
        .order_by(TurnoverScore.score.desc())
        .all()
    )

    return [
        {
            "employee_id": employee.id,
            "name": employee.name,
            "department": employee.department,
            "role": employee.role,
            "score": score.score,
            "risk_level": score.risk_level,
            "calculated_at": score.calculated_at,
        }
        for employee, score in rows
    ]


@router.get("/history/{employee_id}")
def get_score_history(employee_id: int, db: Session = Depends(get_db)):
    employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found",
        )

    scores = (
        db.query(TurnoverScore)
        .filter(TurnoverScore.employee_id == employee_id)
        .order_by(TurnoverScore.calculated_at.desc())
        .all()
    )

    return [
        {
            "id": score.id,
            "employee_id": score.employee_id,
            "score": score.score,
            "risk_level": score.risk_level,
            "calculated_at": score.calculated_at,
        }
        for score in scores
    ]
