from typing import Optional

import jwt
from fastapi import HTTPException, Security, Depends, security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer, OAuth2PasswordBearer
from jose import JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from api import schemas
from api.employee import controllers
from api.schemas import TokenData, Employee, Token
from utils import models
from utils.database import get_db


class AuthHandler:
    __security = HTTPBearer()
    __pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    __secret = 'SECRET'
    __oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

    @staticmethod
    def get_password_hash(password):
        return AuthHandler.__pwd_context.hash(password)

    @staticmethod
    def verify_password(plain_password, hashed_password):
        return AuthHandler.__pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def authenticate_user(db: Session, email: str, password: str):
        user = controllers.get_employee_by_email(db, email)
        if not user:
            return False
        if not AuthHandler.verify_password(password, user.hashed_password):
            return False
        return user

    @staticmethod
    def create_access_token(data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=60)
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, AuthHandler.__secret, algorithm="HS256")

    @staticmethod
    async def get_current_user(db: Session = Depends(get_db), token: str = Depends(__oauth2_scheme)) -> models.Employee:
        print(token)
        payload = jwt.decode(token, AuthHandler.__secret, algorithms=["HS256"])
        emp_email: str = payload.get("sub")
        exp: datetime = payload.get("exp")
        if emp_email is None:
            raise HTTPException(401, "Could not validate credentials", {"WWW-Authenticate": "Bearer"})
        if exp < datetime.utcnow():
            raise HTTPException(401, "Session expired", {"WWW-Authenticate": "Bearer"})
        user = controllers.get_employee_by_email(db, emp_email)
        if user is None:
            raise HTTPException(401, "Could not validate credentials", {"WWW-Authenticate": "Bearer"})
        return user
