from datetime import date
from typing import Optional

from pydantic import BaseModel, ConfigDict


class EmployeeCreate(BaseModel):
    name: str
    department: str
    role: str
    salary: float
    hire_date: date


class EmployeeUpdate(BaseModel):
    name: Optional[str] = None
    department: Optional[str] = None
    role: Optional[str] = None
    salary: Optional[float] = None
    hire_date: Optional[date] = None


class EmployeeResponse(BaseModel):
    id: int
    name: str
    department: str
    role: str
    salary: float
    hire_date: date

    model_config = ConfigDict(from_attributes=True)
