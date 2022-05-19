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

tag: str = "Auth"

@router.post('/', tags=[tag], summary="Authentication in app",
             response_model=LoginSchemaOut)
async def login(login_schema_in: LoginSchemaIn,
                session: Session = Depends(get_db),
                settings: Settings = Depends(get_settings)
                ):
    user: User = User.query(session).filter_by(email=login_schema_in.username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="error email or password invalid")
    if not verify_password(user.password_hash, login_schema_in.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="error email or password invalid")
    access_token_expires = timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        settings,
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return LoginSchemaOut(access_token=access_token, token_type="bearer")


@router.get("/me", tags=[tag], summary="Returns data of logged user", response_model=UserOut)
async def me(current_user: User = Depends(get_current_user)):
    result = UserOut.from_orm(current_user)
    return result
