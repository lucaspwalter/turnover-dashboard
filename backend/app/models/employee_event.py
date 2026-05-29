from sqlalchemy import Column, Date, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.db.database import Base


class EmployeeEvent(Base):
    __tablename__ = "employee_events"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False, index=True)
    event_type = Column(String, nullable=False)
    event_date = Column(Date, nullable=False)
    notes = Column(Text, nullable=True)

    employee = relationship("Employee", back_populates="events")
