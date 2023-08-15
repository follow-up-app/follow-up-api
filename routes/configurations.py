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
from core.security import check_is_admin_user, check_is_parents_user, hash_password, verify_password, create_access_token, get_current_user
from db import get_db
from db.models import User, SpecialtyInstructor
from schemas.configuration_schemas import SpecialtyIn, SpecialtyOut


router = APIRouter()

tags: str = "Configurations"


@router.post('/specialty', summary='Create specialty', response_model=SpecialtyOut, tags=[tags])
async def create(specialty_in: SpecialtyIn, current_user: User = Depends(check_is_admin_user), session: Session = Depends(get_db)):
    specialty = SpecialtyInstructor(
        company_id=current_user.company_id,
        specialty=specialty_in.specialty.upper(),
    )
    session.add(specialty)
    session.commit()

    return SpecialtyOut.from_orm(specialty)


@router.get('/specialty', summary='Return specialty list', response_model=List[SpecialtyOut], tags=[tags])
async def get_all(current_user: User = Depends(check_is_admin_user), session: Session = Depends(get_db)):
    all_itens = SpecialtyInstructor.query(session).all()
    return [SpecialtyOut.from_orm(x) for x in all_itens]


@router.put('/specialty/{id}', summary='Update specialty', tags=[tags], response_model=SpecialtyOut)
async def update(id: UUID, specialty_in: SpecialtyIn, current_user: User = Depends(check_is_admin_user), session: Session = Depends(get_db)):
    specialty: SpecialtyInstructor = SpecialtyInstructor.query(
        session).filter(SpecialtyInstructor.id == id).first()
    if not specialty:
         raise HTTPException(status_code=404, detail='route not found')
    
    specialty.specialty = specialty_in.specialty.upper()
    session.add(specialty)
    session.commit()

    return SpecialtyOut.from_orm(specialty)


@router.delete('/{id}', summary='Delete instuctor',  tags=[tags])
async def delete(id: UUID, current_user: User = Depends(check_is_admin_user), session: Session = Depends(get_db)):
    specialty: SpecialtyInstructor = SpecialtyInstructor.query(
        session).filter(SpecialtyInstructor.id == id).first()
    if not specialty:
         raise HTTPException(status_code=404, detail='route not found')
    session.delete(specialty)
    session.commit()

    return True
