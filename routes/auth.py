from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status
from config import get_settings, Settings
from core.security import verify_password, create_access_token, get_current_user
from db import get_db
from db.models import User
from schemas.user_schemas import UserOut, LoginSchemaIn, LoginSchemaOut

router = APIRouter()

tag: str = "Auth"

@router.post('/', tags=[tag], summary="Authentication in app",
             response_model=LoginSchemaOut)
async def login(login_schema_in: LoginSchemaIn,
                session: Session = Depends(get_db),
                settings: Settings = Depends(get_settings)
                ):
    user: User = User.query(session).filter_by(
        email=login_schema_in.username).first()
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
    
    return LoginSchemaOut(access_token=access_token, token_type="bearer", expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES)


@router.get("/refresh", tags=[tag], summary="Refresh token of logged user", response_model=LoginSchemaOut)
async def refresh(current_user: User = Depends(get_current_user), settings: Settings = Depends(get_settings)):
    access_token_expires = timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        settings,
        data={"sub": current_user.email}, expires_delta=access_token_expires
    )
    return LoginSchemaOut(access_token=access_token, token_type="bearer", expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES)


@router.get("/me", tags=[tag], summary="Returns data of logged user", response_model=UserOut)
async def me(current_user: User = Depends(get_current_user)):
    result = UserOut.from_orm(current_user)
    return result
