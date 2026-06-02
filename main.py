from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
import models
import schemas
from database import Base, engine, get_db

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Leave Management System")

@app.get("/")
def home():
    return {"message": "Leave Management System API Running"}


# ---------------- EMPLOYEE MANAGEMENT ----------------

@app.post("/employees")
def add_employee(employee: schemas.EmployeeCreate, db: Session = Depends(get_db)):

    existing_employee = db.query(models.Employee).filter(
        models.Employee.email == employee.email
    ).first()

    if existing_employee:
        raise HTTPException(status_code=400, detail="Email already exists")

    new_employee = models.Employee(**employee.dict())

    db.add(new_employee)
    db.commit()
    db.refresh(new_employee)

    return {
        "message": "Employee added successfully",
        "employee_id": new_employee.employee_id
    }


@app.get("/employees")
def view_employees(
    search: str = "",
    department: str = "",
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1),
    db: Session = Depends(get_db)
):

    query = db.query(models.Employee)

    if search:
        query = query.filter(models.Employee.name.like(f"%{search}%"))

    if department:
        query = query.filter(models.Employee.department == department)

    total = query.count()

    employees = query.offset((page - 1) * limit).limit(limit).all()

    return {
        "total": total,
        "page": page,
        "employees": employees
    }


@app.get("/employees/{employee_id}")
def get_employee(employee_id: int, db: Session = Depends(get_db)):

    employee = db.query(models.Employee).filter(
        models.Employee.employee_id == employee_id
    ).first()

    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    return employee

@app.put("/employees/{employee_id}")
def update_employee(
    employee_id: int,
    employee: schemas.EmployeeUpdate,
    db: Session = Depends(get_db)):

    db_employee = db.query(models.Employee).filter(
        models.Employee.employee_id == employee_id
    ).first()

    if not db_employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    for key, value in employee.dict(exclude_unset=True).items():
        setattr(db_employee, key, value)

    db.commit()

    return {"message": "Employee updated successfully"}


@app.delete("/employees/{employee_id}")
def delete_employee(employee_id: int, db: Session = Depends(get_db)):

    employee = db.query(models.Employee).filter(
        models.Employee.employee_id == employee_id
    ).first()

    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    db.delete(employee)
    db.commit()

    return {"message": "Employee deleted successfully"}


# ---------------- LEAVE MANAGEMENT ----------------

@app.post("/leave")
def apply_leave(leave: schemas.LeaveCreate, db: Session = Depends(get_db)):

    employee = db.query(models.Employee).filter(
        models.Employee.employee_id == leave.employee_id
    ).first()

    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    if leave.end_date < leave.start_date:
        raise HTTPException(
            status_code=400,
            detail="End date cannot be before start date"
        )

    overlapping_leave = db.query(models.LeaveRequest).filter(
        models.LeaveRequest.employee_id == leave.employee_id,
        models.LeaveRequest.start_date <= leave.end_date,
        models.LeaveRequest.end_date >= leave.start_date
    ).first()

    if overlapping_leave:
        raise HTTPException(
            status_code=400,
            detail="Overlapping leave request exists"
        )

    new_leave = models.LeaveRequest(**leave.dict())

    db.add(new_leave)
    db.commit()

    return {"message": "Leave applied successfully"}


@app.get("/leaves")
def view_leave_requests(
    status: str = "",
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1),
    db: Session = Depends(get_db)
):

    query = db.query(models.LeaveRequest)

    if status:
        query = query.filter(models.LeaveRequest.status == status)

    total = query.count()

    leaves = query.offset((page - 1) * limit).limit(limit).all()

    return {
        "total": total,
        "page": page,
        "leave_requests": leaves
    }


@app.put("/leave/{leave_id}")
def update_leave_status(
    leave_id: int,
    update: schemas.LeaveStatusUpdate,
    db: Session = Depends(get_db)
):

    leave = db.query(models.LeaveRequest).filter(
        models.LeaveRequest.leave_id == leave_id
    ).first()

    if not leave:
        raise HTTPException(status_code=404, detail="Leave request not found")

    if leave.status == "Approved":
        raise HTTPException(
            status_code=400,
            detail="Approved leaves cannot be modified"
        )

    if update.status not in ["Approved", "Rejected"]:
        raise HTTPException(
            status_code=400,
            detail="Status must be Approved or Rejected"
        )

    leave.status = update.status

    db.commit()

    return {"message": f"Leave {update.status.lower()} successfully"}


@app.get("/employee-history/{employee_id}")
def employee_leave_history(
    employee_id: int,
    db: Session = Depends(get_db)
):
    employee = db.query(models.Employee).filter(
        models.Employee.employee_id == employee_id
    ).first()

    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    history = db.query(models.LeaveRequest).filter(
        models.LeaveRequest.employee_id == employee_id
    ).all()

    return history
