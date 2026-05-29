from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.database import Base


class TurnoverScore(Base):
    __tablename__ = "turnover_scores"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False, index=True)
    score = Column(Float, nullable=False)
    risk_level = Column(String, nullable=False)
    calculated_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    employee = relationship("Employee", back_populates="turnover_scores")
