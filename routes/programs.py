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
from core.security import check_is_admin_user, check_is_instructor_user, check_is_parents_user, hash_password, verify_password, create_access_token, get_current_user
from db import get_db
from db.models import Program, User
from schemas.program_schemas import ProgramIn, ProgramOut

router = APIRouter()

tags: str = "Program"


@router.post('/', summary='Create program', tags=[tags])
async def create(program_in: ProgramIn, current_user: User = Depends(check_is_admin_user), session: Session = Depends(get_db)):
    program = Program(
        company_id=current_user.company_id,
        title=program_in.title,
        objective=program_in.objective,
    )
    session.add(program)
    session.commit()

    return ProgramOut.from_orm(program)


@router.get('/', summary='Returns programs list', response_model=List[ProgramOut], tags=[tags])
async def get_all(current_user: User = Depends(check_is_admin_user), session: Session = Depends(get_db)):
    all_itens = Program.query(session).all()
    return [ProgramOut.from_orm(x) for x in all_itens]


@router.get('/{id}', summary='Returns program', tags=[tags])
async def get_id(id: UUID, current_user: User = Depends(check_is_admin_user), session: Session = Depends(get_db)):
    program: Program = Program.query(session).filter(Program.id == id).first()
    if not program:
        raise HTTPException(status_code=404, detail='route not found')

    return [ProgramOut.from_orm(program)]


@router.put('/{id}', summary='Update program', tags=[tags])
async def update(id: UUID, program_in: ProgramIn, current_user: User = Depends(check_is_admin_user), session: Session = Depends(get_db)):
    program = Program(
        company_id=current_user.company_id,
        title=program_in.title,
        objetive=program_in.objetive,
    )
    session.add(program)
    session.commit()

    return ProgramOut.from_orm(program)

@router.delete('/{id}', summary='Delete program', response_model=List[ProgramOut], tags=[tags])
async def delete(id: UUID, current_user: User = Depends(check_is_admin_user), session: Session = Depends(get_db)):
    pass
