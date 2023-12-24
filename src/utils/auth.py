from typing import Optional

import jwt
from fastapi import HTTPException, Security, Depends, security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer, OAuth2PasswordBearer
from jose import JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from api.employee import controllers
from api.schemas import Token, Employee


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
    def create_access_token(data: dict):
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=60)
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, AuthHandler.__secret)

    @staticmethod
    async def get_current_user(db: Session, token: str = Depends(__oauth2_scheme)):
        payload = jwt.decode(token, AuthHandler.__secret, algorithms=["HS256"])
        username: str = payload.get("sub")
        exp: datetime = payload.get("exp")
        if username is None:
            raise HTTPException(401, "Could not validate credentials", {"WWW-Authenticate": "Bearer"})
        if exp < datetime.utcnow():
            raise HTTPException(401, "Session expired", {"WWW-Authenticate": "Bearer"})
        token_data = Token(username=username)
        user = controllers.get_employee_detail(db, id=token_data.employee_id)
        if user is None:
            raise HTTPException(401, "Could not validate credentials", {"WWW-Authenticate": "Bearer"})
        return user

    @staticmethod
    async def get_current_active_user(db: Session, current_user: Employee = Depends(get_current_user)):
        return controllers.get_employee_detail(db, current_user.id)
