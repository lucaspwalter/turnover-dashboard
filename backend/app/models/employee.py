from sqlalchemy import Column, Date, Float, Integer, String
from sqlalchemy.orm import relationship

from app.db.database import Base


class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    department = Column(String, nullable=False)
    role = Column(String, nullable=False)
    salary = Column(Float, nullable=False)
    hire_date = Column(Date, nullable=False)

    turnover_scores = relationship("TurnoverScore", back_populates="employee")
    events = relationship("EmployeeEvent", back_populates="employee")
