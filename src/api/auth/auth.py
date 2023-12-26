import jwt
from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from api import schemas
from api.employee import employee_controllers as cr
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
    def authenticate_user(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
        exception = HTTPException(401, "Incorrect username or password", {"WWW-Authenticate": "Bearer"})
        user = cr.get_employee_by_email(db, form_data.username)
        if not user or not AuthHandler.verify_password(form_data.password, user.hashed_password):
            raise exception
        access_token = AuthHandler.create_access_token(data={"sub": user.email})
        token_data = {"access_token": access_token, "token_type": "bearer"}
        cr.add_token(db, user, schemas.TokenBase(**token_data))
        return token_data

    @staticmethod
    def create_access_token(data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=60)
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, AuthHandler.__secret, algorithm="HS256")

    @staticmethod
    async def get_current_user(db: Session = Depends(get_db), token: str = Depends(__oauth2_scheme)) -> models.Employee:
        payload = jwt.decode(token, AuthHandler.__secret, algorithms=["HS256"])
        emp_email: str = payload.get("sub")
        exp: int = payload.get("exp")
        if emp_email is None:
            raise HTTPException(401, "Could not validate credentials", {"WWW-Authenticate": "Bearer"})
        if exp < datetime.utcnow().timestamp():
            raise HTTPException(401, "Session expired", {"WWW-Authenticate": "Bearer"})
        user = cr.get_employee_by_email(db, emp_email)
        if user is None:
            raise HTTPException(401, "Could not validate credentials", {"WWW-Authenticate": "Bearer"})
        return user
