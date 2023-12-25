from enum import Enum
from fastapi import HTTPException
from typing import List

from fastapi import Depends, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from api import schemas
from api.auth.auth import AuthHandler
from utils.database import session
from api.employee import controllers as cr
from utils import models
from utils.database import get_db

employee_router = APIRouter()

tags: List[str | Enum] = ["employee"]


@employee_router.post("/signup", response_model=schemas.EmployeeBase, tags=tags)
async def signup(employee: schemas.EmployeeCreate, db: Session = Depends(get_db)):
    return cr.create_employee(db=db, employee=employee)


@employee_router.post("/token", response_model=schemas.TokenBase, tags=tags)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = AuthHandler.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(401, "Incorrect username or password", {"WWW-Authenticate": "Bearer"})

    access_token = AuthHandler.create_access_token(data={"sub": user.email})
    token = {"access_token": access_token, "token_type": "bearer"}
    cr.create_token(db, user, schemas.TokenBase(**token))
    return token


@employee_router.get("/users/me/", response_model=schemas.Employee, tags=tags)
async def read_users_me(current_user: schemas.Employee = Depends(AuthHandler.get_current_user)):
    return current_user
