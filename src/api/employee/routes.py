from enum import Enum
from typing import List

from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session

from api import schemas
from api.auth.auth import AuthHandler
from api.employee import controllers as cr
from utils.database import get_db

employee_router = APIRouter()

tags: List[str | Enum] = ["employee"]


@employee_router.post("/signup", response_model=schemas.EmployeeBase, tags=tags)
async def signup(employee: schemas.EmployeeCreate, db: Session = Depends(get_db)):
    return cr.create_employee(db=db, employee=employee)


@employee_router.post("/login", response_model=schemas.TokenBase, tags=tags)
async def login_for_access_token(token: schemas.TokenBase = Depends(AuthHandler.authenticate_user)):
    return token


@employee_router.get("/users/me/", response_model=schemas.Employee, tags=tags)
async def read_users_me(current_user: schemas.Employee = Depends(AuthHandler.get_current_user)):
    return current_user
