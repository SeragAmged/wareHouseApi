from typing import List

from fastapi import HTTPException
from sqlalchemy.orm import Session

import api.branch.branch_controllers
from api import schemas
from api.auth import auth
from utils import models, validators


def get_employee_by_id(db: Session, id: int) -> models.Employee | None:
    return db.query(models.Employee).filter(models.Employee.id == id).first()


def get_employee_by_sesa(db: Session, sesa_id: int) -> models.Employee | None:
    return db.query(models.Employee).filter(models.Employee.sesa_id == sesa_id).first()


def get_employee_by_phone(db: Session, phone: str) -> models.Employee | None:
    return (db.query(models.Employee).filter(models.Employee.phone == phone).first())


def get_employee_by_email(db: Session, email: str) -> models.Employee | None:
    return db.query(models.Employee).filter(models.Employee.email == email).first()


def get_all_employees(db: Session, skip: int = 0, limit: int = 100) -> List[models.Employee]:
    return db.query(models.Employee).order_by(models.Employee.sesa_id).offset(skip).limit(limit).all()


def verify_employee_exists(employee: models.Employee) -> models.Employee:
    if employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee


def verify_attributes(db: Session, employee: schemas.EmployeeBase) -> None:
    if not validators.is_sesa_id_valid(employee.sesa_id):
        raise HTTPException(
            422, {"error": "Given sesa id is invalid", "field": "sesa_id"})
    if not validators.is_valid_email(employee.email):
        raise HTTPException(
            422, {"error": "Given email is invalid", "field": "email"})
    if get_employee_by_sesa(db, employee.sesa_id):
        raise HTTPException(
            422, {"error": "Employee with same sesa ID already registered", "field": "sesa_id"})
    if employee.phone and get_employee_by_phone(db, employee.phone):
        raise HTTPException(
            422, {"error": "Employee with same phone number already registered", "field": "phone"})
    if get_employee_by_email(db, employee.email):
        raise HTTPException(
            422, {"error": "Employee with same email address already registered", "field": "email"})
    # if api.branch.controllers.get_branch_by_id(db, employee.branch_id) is None:
    #     raise HTTPException(
    #         422, {"error": "Branch doesn't exist", "field": "branch"})


def create_employee(db: Session, employee: schemas.EmployeeCreate) -> models.Employee:
    verify_attributes(db, employee)
    emp_model = employee.model_dump()
    branch_test = api.branch.branch_controllers.get_branch_by_name(
        db=db, name=emp_model["branch_name"])
    if branch_test is None:
        raise HTTPException(status_code=404, detail="branch is Not found")
    emp_model['branch_id'] = branch_test.id;
    emp_model["hashed_password"] = auth.AuthHandler.get_password_hash(
        emp_model["password"])
    del emp_model["password"]
    del emp_model["branch_name"]
    db_employee = models.Employee(**emp_model)
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    return db_employee


def update_employee(db: Session, employee: schemas.EmployeeCreate):
    verify_attributes(db, employee)
    for key, value in employee.model_dump().items():
        setattr(employee, key, value)
    db.commit()
    db.refresh(employee)
    return employee


def delete_employee(db: Session, sesa_id: int) -> None:
    # TODO: check if user has the permission to delete
    if get_employee_by_sesa(db=db, sesa_id=sesa_id) is None:
        raise HTTPException(
            401, "Employee doesn't exist (How did you get here?")
    db_employee = db.query(models.Employee).filter(
        models.Employee.sesa_id == sesa_id).first()
    db.delete(db_employee)
    db.commit()


def add_token(db: Session, employee: schemas.Employee, token_base: schemas.TokenBase) -> models.Token:
    token_dumb = token_base.model_dump()
    token_dumb["employee"] = employee
    db_token = models.Token(**token_dumb)
    db.add(db_token)
    db.commit()
    db.refresh(db_token)
    return db_token


def delete_token(db: Session, token: str):
    db_token = db.query(models.Token).filter(models.Token.access_token == token).first()
    if db_token:
        db.delete(db_token)
        db.commit()


# TODO: ONLY FOR ADMINS
# if user register with sesa_id in the admins.txt file set his role to admin(NOTE:each line contains sesa_id)
# ⬆️ ^^ use deferent function for reading the admins file and store it in the memory(variable)


