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
from config import get_settings, Settings
from app.core.security import check_is_admin_user, check_is_parents_user, hash_password, verify_password, create_access_token, get_current_user
from db import get_db
from db.models import User
from app.schemas.configuration_schemas import SpecialtyIn, SpecialtyOut


router = APIRouter()

tags: str = "Configurations"


@router.post('/specialty', summary='Create specialty', response_model=SpecialtyOut, tags=[tags])
async def create(specialty_in: SpecialtyIn, current_user: User = Depends(check_is_admin_user), session: Session = Depends(get_db)):
   pass


@router.get('/specialty', summary='Return specialty list', response_model=List[SpecialtyOut], tags=[tags])
async def get_all(current_user: User = Depends(check_is_admin_user), session: Session = Depends(get_db)):
    pass


@router.put('/specialty/{id}', summary='Update specialty', tags=[tags], response_model=SpecialtyOut)
async def update(id: UUID, specialty_in: SpecialtyIn, current_user: User = Depends(check_is_admin_user), session: Session = Depends(get_db)):
    pass


@router.delete('/{id}', summary='Delete instuctor',  tags=[tags])
async def delete(id: UUID, current_user: User = Depends(check_is_admin_user), session: Session = Depends(get_db)):
   pass
