from datetime import timedelta, datetime

from typing import Optional

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import cume_dist, current_date, current_user
from starlette import status

from config import Settings, get_settings
from db import get_db
from db.models import User, UserPermission
import datetime
from core.utils import now
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/users/login')
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(stored_password: str, provided_password: str) -> bool:
    return pwd_context.verify(provided_password, stored_password)


def create_access_token(settings: Settings, data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = now() + expires_delta
    else:
        expire = now() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def get_current_user(token: str = Depends(oauth2_scheme), session: Session = Depends(get_db),
                     settings: Settings = Depends(get_settings)) -> User:
    try:
        declined_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not logged yet")
        decoded = jwt.decode(token, key=settings.SECRET_KEY,
                             algorithms=[settings.ALGORITHM])
        email: str = decoded.get('sub')

        current_user: User = session.query(User)\
            .filter(User.deleted == False)\
            .filter_by(email=email).first()
        if not current_user:
            raise declined_exception

        return current_user
    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired")


def check_permission(current_user: User, user_permission: UserPermission):
    declined_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                       detail="You dont have access to resource")
    list_permited = []
    
    if user_permission == UserPermission.ADMIN:
        list_permited.append(UserPermission.ADMIN)
        list_permited.append(UserPermission.INSTRUCTOR)
        list_permited.append(UserPermission.PARENTS)

    if user_permission == UserPermission.INSTRUCTOR:
        list_permited.append(UserPermission.INSTRUCTOR)
        list_permited.append(UserPermission.PARENTS)

    if user_permission == UserPermission.PARENTS:
        list_permited.append(UserPermission.PARENTS)

    if current_user.permission in list_permited:
        return current_user
    
    raise declined_exception


def check_is_admin_user(current_user: User = Depends(get_current_user)):
    return check_permission(current_user, UserPermission.ADMIN)

def check_is_instructor_user(current_user: User = Depends(get_current_user)):
    return check_permission(current_user, UserPermission.INSTRUCTOR)

def check_is_parents_user(current_user: User = Depends(get_current_user)):
    return check_permission(current_user, UserPermission.PARENTS)

# def check_is_student_user(current_user: User = Depends(get_current_user)):
#     return check_permission(current_user, UserPermission.STUDANTS)