from sqlalchemy.orm import Session

from app.models.employee import Employee
from app.models.employee_event import EmployeeEvent
from app.models.turnover_score import TurnoverScore
from app.schemas.employee import EmployeeCreate, EmployeeUpdate


def get_all(db: Session, department: str | None = None, risk_level: str | None = None):
    query = db.query(Employee)

    if department:
        query = query.filter(Employee.department == department)

    if risk_level:
        query = (
            query.join(TurnoverScore)
            .filter(TurnoverScore.risk_level == risk_level)
            .distinct()
        )

    return query.all()


def get_by_id(db: Session, employee_id: int):
    return db.query(Employee).filter(Employee.id == employee_id).first()


def create(db: Session, employee_data: EmployeeCreate):
    employee = Employee(**employee_data.model_dump())
    db.add(employee)
    db.commit()
    db.refresh(employee)
    return employee


def update(db: Session, employee_id: int, employee_data: EmployeeUpdate):
    employee = get_by_id(db, employee_id)
    if not employee:
        return None

    for field, value in employee_data.model_dump(exclude_unset=True).items():
        setattr(employee, field, value)

    db.commit()
    db.refresh(employee)
    return employee


def delete(db: Session, employee_id: int):
    employee = get_by_id(db, employee_id)
    if not employee:
        return False

    db.query(EmployeeEvent).filter(EmployeeEvent.employee_id == employee_id).delete(
        synchronize_session=False
    )
    db.query(TurnoverScore).filter(TurnoverScore.employee_id == employee_id).delete(
        synchronize_session=False
    )
    db.delete(employee)
    db.commit()
    return True
