from enum import Enum
from typing import List, Dict

from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session

from api import schemas
from api.auth.auth import AuthHandler
from api.employee import employee_controllers as cr
from utils.database import get_db

employee_router = APIRouter()

tags: List[str | Enum] = ["employee"]


@employee_router.post("/signup", response_model=schemas.Employee, tags=tags)
async def signup(employee: schemas.EmployeeCreate, db: Session = Depends(get_db)):
    return cr.create_employee(db=db, employee=employee)


@employee_router.post("/login", response_model=schemas.TokenBase, tags=tags)
async def login_with_oauth2(token: schemas.TokenBase = Depends(AuthHandler.authenticate_user)):
    return token


@employee_router.get("/employees/me", response_model=schemas.Employee, tags=tags)
async def read_users_me(current_user: schemas.Employee = Depends(AuthHandler.get_current_user)):
    return current_user


@employee_router.post("/signout", tags=tags)
async def signout(token: schemas.TokenBase = Depends(AuthHandler.revoke_token)):
    return {"message": "Successfully signed out"}


@employee_router.get('/employees', response_model=List[schemas.Employee], tags=tags)
async def get_employees(db: Session = Depends(get_db)):
    return cr.get_all_employees(db=db)


@employee_router.get("/employees/{sesa_id}", response_model=schemas.Employee, tags=tags)
async def get_employee(sesa_id: str, db: Session = Depends(get_db), current_user: schemas.Employee = Depends(read_users_me)):
    return cr.verify_employee_exists(cr.get_employee_by_sesa(db=db, sesa_id=int(sesa_id)))


@employee_router.put('/employees/{sesa_id}', response_model=schemas.Employee, tags=tags)
async def update_employee(sesa_id: str, employee: schemas.EmployeeCreate, db: Session = Depends(get_db), current_user: schemas.Employee = Depends(read_users_me)):
    db_employee = cr.get_employee_by_sesa(db, int(sesa_id))
    if db_employee is None:
        raise HTTPException(401, "Employee doesn't exist.")
    if db_employee.sesa_id != current_user.sesa_id and current_user.role != "admin":  # type: ignore
        raise HTTPException(
            403, "You don't have permission to edit this account!")
    return cr.update_employee(db=db, employee=employee)
