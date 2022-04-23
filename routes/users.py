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

@router.post('/', tags=[user_tag], 
            summary='Create user', 
            description='Method for create user',
            )
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
      password_hash = hash_password(password), 
      fullname = user_schema.fullname,
      email = user_schema.email,
      document = user_schema.document,
      permission = user_schema.permission,
      first_access = True,
    )
    session.add(user)
    session.commit()

    return {'status_code': 200, 'message': 'Success'}

