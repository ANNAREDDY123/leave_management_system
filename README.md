# Leave Management System

## Objective

Backend system to manage Employees and Leave Requests using FastAPI and SQL.

## Tech Stack

- Python 3
- FastAPI
- SQLAlchemy
- Pydantic
- SQLite / MySQL

## Features

### Employee Management
- Add Employee
- View Employees
- Get Employee by ID
- Update Employee
- Delete Employee
- Search by Name
- Search by Department
- Pagination

### Leave Management
- Apply Leave
- View Leave Requests
- Approve Leave
- Reject Leave
- View Employee Leave History
- Filter by Status

### Business Rules
- Employee must exist before applying leave
- End date cannot be before start date
- Prevent overlapping leave requests
- Approved leaves cannot be modified

### SQL Reports
- Highest Number of Leaves
- Department-wise Leave Count
- Pending Leave Requests
- Monthly Leave Report
- Employees Who Never Applied for Leave
- Employee Ranking using Window Functions

## Project Structure

leave_management_system/
├── main.py
├── database.py
├── models.py
├── schemas.py
├── requirements.txt
├── README.md
├── sql/
│   ├── schema.sql
│   └── report_queries.sql
└── postman_collection.json

## Run Project

pip install -r requirements.txt
uvicorn main:app 

Swagger:

http://127.0.0.1:8000/docs

Explanation

I created two tables: Employees and Leave Requests.

Employees store employee details such as name, email, department, and designation.

Leave Requests store leave application information including leave type, dates, reason, and approval status.

Business rules ensure employees exist before applying, dates are valid, overlapping leaves are prevented, and approved leaves cannot be modified.

FastAPI provides Swagger documentation automatically, while SQL queries generate reports and analytics.

Submission Files
Source Code
SQL Schema Script
SQL Report Queries
Postman Collection
README

