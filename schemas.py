from pydantic import BaseModel, Field
from typing import Optional
from datetime import date

class EmployeeCreate(BaseModel):
    name: str = Field(min_length=2)
    email: str
    department: str
    designation: str

class EmployeeUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    department: Optional[str] = None
    designation: Optional[str] = None

class LeaveCreate(BaseModel):
    employee_id: int
    leave_type: str
    start_date: date
    end_date: date
    reason: str

class LeaveStatusUpdate(BaseModel):
    status: str
