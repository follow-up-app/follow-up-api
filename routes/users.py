from datetime import timedelta
from typing import List
from uuid import UUID
from sqlalchemy import or_
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from itsdangerous import URLSafeTimedSerializer
from sqlalchemy.orm import Session
from starlette import status
from starlette.background import BackgroundTasks
import re
import os
import unidecode

from config import get_settings, Settings
from core.security import check_is_admin_user, hash_password, verify_password, create_access_token, get_current_user
from db import get_db
from db.models import User, UserPermission
from schemas.user_schemas import UserOut, ResetPasswordSchemaIn, ResetPasswordSchemaOut, \
    RecoveryPasswordSchemaIn, RecoveryPasswordSchemaOut, LoginSchemaIn, LoginSchemaOut, \
    UserRegisterSchemaIn, UserStoreIn


router = APIRouter()

user_tag: str = "Users"


async def get_user(session: Session, email: str) -> User:
    user = User.query(session).filter_by(email=email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="user does not exists")
    return user


@router.post('/', tags=[user_tag], summary='Create user', description='Method for create user')
async def register(user_schema: UserStoreIn, session: Session = Depends(get_db),
                   settings: Settings = Depends(get_settings)):
    user = User.query(session).filter(or_(
        User.document == user_schema.document,
        User.email == user_schema.email)).first()
    if user:
        raise HTTPException(
            status_code=403, detail="user_already_exists")

    password = '123'

    user = User(
        company_id=user_schema.company_id,
        password_hash=hash_password(password),
        fullname=user_schema.fullname,
        email=user_schema.email,
        document=user_schema.document,
        permission=user_schema.permission,
    )
    session.add(user)
    session.commit()

    return UserOut.from_orm(user)


@router.get('/', summary='Returns users list', response_model=List[UserOut], tags=[user_tag])
async def get_all(session: Session = Depends(get_db)):
    all_itens = User.query(session).all()
    return [UserOut.from_orm(x) for x in all_itens]


@router.get('/{id}', summary='Returns user', response_model=List[UserOut], tags=[user_tag])
async def get_id(id: UUID, current_user: User = Depends(check_is_admin_user), session: Session = Depends(get_db)):
    user: User = User.query(session).filter(User.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail='route not found')

    return [UserOut.from_orm(user)]


@router.put('/{id}', summary='Update user', response_model=List[UserOut], tags=[user_tag])
async def update(id: UUID, user_schema: UserStoreIn, current_user: User = Depends(check_is_admin_user), session: Session = Depends(get_db)):
    password = '123'

    user = User(
        company_id=user_schema.company_id,
        password_hash=hash_password(password),
        fullname=user_schema.fullname,
        email=user_schema.email,
        document=user_schema.document,
        permission=user_schema.permission,
    )
    session.add(user)
    session.commit()

    return UserOut.from_orm(user)


@router.delete('/{id}', summary='Delete user', response_model=List[UserOut], tags=[user_tag])
async def delete(id: UUID, current_user: User = Depends(check_is_admin_user), session: Session = Depends(get_db)):
    pass


@router.post('/login/', tags=[user_tag], summary="Authentication in app",
             response_model=LoginSchemaOut)
async def login(login_schema_in: LoginSchemaIn,
                session: Session = Depends(get_db),
                settings: Settings = Depends(get_settings)
                ):
    user: User = User.query(session).filter_by(email=login_schema_in.email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="error username or password invalid")
    if not verify_password(user.password_hash, login_schema_in.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="error username or password invalid")
    access_token_expires = timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        settings,
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return LoginSchemaOut(access_token=access_token, token_type="bearer")


@router.get("/me/", tags=[user_tag], summary="Returns data of logged user", response_model=UserOut)
async def me(current_user: User = Depends(get_current_user)):
    result = UserOut.from_orm(current_user)
    return result


