from enum import Enum
from http.client import HTTPException
from typing import List

from fastapi import Depends, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from api import schemas
from utils.auth import AuthHandler
from utils.database import session

router = APIRouter()

tags: List[str | Enum] = ["employee"]


def get_db():
    db = session
    try:
        yield db
    finally:
        db.close()


@router.post("/token", response_model=schemas.Token, tags=tags)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = AuthHandler.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(401, "Incorrect username or password", {"WWW-Authenticate": "Bearer"})

    access_token = AuthHandler.create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/employees/me", response_model=schemas.Employee, tags=tags)
def read_users_me(current_user: schemas.Employee = Depends(AuthHandler.get_current_active_user)):
    return current_user
