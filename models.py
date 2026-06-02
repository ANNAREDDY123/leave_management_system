from sqlalchemy import Column, Integer, String, ForeignKey, Date
from database import Base

class Employee(Base):
    __tablename__ = "employees"

    employee_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    department = Column(String(100), nullable=False)
    designation = Column(String(100), nullable=False)

class LeaveRequest(Base):
    __tablename__ = "leave_requests"

    leave_id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.employee_id"))
    leave_type = Column(String(50), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    reason = Column(String(255))
    status = Column(String(20), default="Pending")
