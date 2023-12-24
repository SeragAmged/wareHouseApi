from typing import List

from fastapi import HTTPException
from sqlalchemy.orm import Session

from api import schemas
from api.auth import auth
from utils import models, validators


def get_employee_by_id(db: Session, id: int) -> models.Employee | None:
    return db.query(models.Employee).filter(models.Employee.id == id).first()


def get_employee_by_sesa(db: Session, sesa_id: int) -> models.Employee | None:
    return db.query(models.Employee).filter(models.Employee.sesa_id == sesa_id).first()


def get_employee_by_phone(db: Session, phone: str) -> models.Employee | None:
    return db.query(models.Employee).filter(models.Employee.phone == phone).first()


def get_employee_by_email(db: Session, email: str) -> models.Employee | None:
    return db.query(models.Employee).filter(models.Employee.email == email).first()


def get_all_employees(db: Session, skip: int = 0, limit: int = 100) -> List[models.Employee]:
    return db.query(models.Employee).offset(skip).limit(limit).all()


def check_uniqueness(db: Session, employee: schemas.EmployeeBase) -> int:
    if get_employee_by_sesa(db, employee.sesa_id):
        return 1
    if employee.phone:
        if get_employee_by_phone(db, employee.phone):
            return 2
    if get_employee_by_email(db, employee.email):
        return 3
    return 0


def create_employee(db: Session, employee: schemas.EmployeeCreate) -> models.Employee:
    if validators.is_sesa_id_valid(employee.sesa_id):
        raise HTTPException(422, {"error": "Given sesa id is invalid", "field": "sesa_id"})
    if validators.is_valid_email(employee.email):
        raise HTTPException(422, {"error": "Given email is invalid", "field": "email"})
    unique = check_uniqueness(db, employee)
    if unique == 1:
        raise HTTPException(422, {"error": "Employee with same sesa ID already registered", "field": "sesa_id"})
    if unique == 2:
        raise HTTPException(422, {"error": "Employee with same phone number already registered", "field": "phone"})
    if unique == 3:
        raise HTTPException(422, {"error": "Employee with same email address already registered", "field": "email"})

    emp_model = employee.model_dump()
    emp_model["hashed_password"] = auth.AuthHandler
    db_employee = models.Employee(**employee.model_dump())
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    return db_employee


def update_employee(db: Session, sesa_id: int, employee: schemas.EmployeeCreate):
    db_employee = get_employee_by_sesa(db=db, sesa_id=sesa_id)
    if db_employee is None:
        raise HTTPException(401, "Employee doesn't exist (How did you get here?")
    # TODO: check if user has the permission to update

    if validators.is_sesa_id_valid(employee.sesa_id):
        raise HTTPException(422, {"error": "Given sesa id is invalid", "field": "sesa_id"})
    if validators.is_valid_email(employee.email):
        raise HTTPException(422, {"error": "Given email is invalid", "field": "email"})
    unique = check_uniqueness(db, employee)
    if unique == 1:
        raise HTTPException(422, {"error": "Employee with same sesa ID already registered", "field": "sesa_id"})
    if unique == 2:
        raise HTTPException(422, {"error": "Employee with same phone number already registered", "field": "phone"})
    if unique == 3:
        raise HTTPException(422, {"error": "Employee with same email address already registered", "field": "email"})

    for key, value in employee.model_dump().items():
        setattr(db_employee, key, value)
    db.commit()
    db.refresh(db_employee)
    return db_employee


def delete_employee(db: Session, sesa_id: int) -> None:
    # TODO: check if user has the permission to delete
    if get_employee_by_sesa(db=db, sesa_id=sesa_id) is None:
        raise HTTPException(401, "Employee doesn't exist (How did you get here?")

    db_employee = db.query(models.Employee).filter(models.Employee.sesa_id == sesa_id).first()
    db.delete(db_employee)
    db.commit()


# TODO:
# add itemDetail
# also add records for it with type from the enums

# delete itemDetail
# also add records for it with type from the enums

# update itemDetail
# also add records for it with type from the enums

# get itemdetail by name
# get itemdetail by id


# Get CURRENT available items

# TODO:add quantity trigger for inserting

# TODO:

# ONLY FOR ADMINS
# ADD EMPLOYEE
# create emp depends on branch name not id (may need edit in model)
# email validation ---@---.--
# if user register with sesa_id in the admins.txt file set his role to admin(NOTE:each line contains sesa_id)
# ⬆️ ^^ use deferent function for reading the admins file and store it in the memory(variable)


# create comment
# book item if it's available
# Check_out item if it's available and change item status to job assigned
# check_in item if he is the one who checked it out
