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
from core.security import check_is_admin_user, check_is_parents_user, hash_password, verify_password, create_access_token, get_current_user
from db import get_db
from db.models import Procedure, User
from schemas.procedure_schemas import ProcedureIn, ProcedureOut


router = APIRouter()

tags: str = "Procedure"

@router.post('/', summary='Create procedure', tags=[tags], response_model=ProcedureOut)
async def create(procedure_in: ProcedureIn, current_user: User = Depends(check_is_admin_user), session: Session = Depends(get_db)):
    procedure = Procedure(
        program_id=procedure_in.program_id,
        name=unidecode.unidecode(procedure_in.name).upper(),
        objective=procedure_in.objective,
        stimulus=procedure_in.stimulus,
        answer=procedure_in.answer,
        consequence = procedure_in.consequence,
        material = procedure_in.material,
        type_help = procedure_in.type_help,
        attempts = procedure_in.attempts,
        goal_value = procedure_in.goal_value,
        description = procedure_in.description,
    )
    session.add(procedure)
    session.commit()

    return ProcedureOut.from_orm(procedure)

@router.get('/', summary='Returns procedures list', response_model=List[ProcedureOut], tags=[tags])
async def get_all(current_user: User = Depends(check_is_admin_user), session: Session = Depends(get_db)):
    all_itens = Procedure.query(session).all()
    return [ProcedureOut.from_orm(x) for x in all_itens]

@router.get('/program/{id}', summary='Returns procedures list in program reference', response_model=List[ProcedureOut], tags=[tags])
async def get_all_program(id: UUID, current_user: User = Depends(check_is_admin_user), session: Session = Depends(get_db)):
    all_itens = Procedure.query(session).filter(Procedure.program_id == id).all()
    return [ProcedureOut.from_orm(x) for x in all_itens]


@router.get('/{id}', summary='Returns procedure', tags=[tags], response_model=ProcedureOut)
async def get_id(id: UUID, current_user: User = Depends(check_is_admin_user), session: Session = Depends(get_db)):
    procedure: Procedure = Procedure.query(session).filter(Procedure.id == id).first()
    if not procedure:
        raise HTTPException(status_code=404, detail='route not found')

    return ProcedureOut.from_orm(procedure)


@router.put('/{id}', summary='Update procedure', tags=[tags], response_model=ProcedureOut)
async def update(id: UUID, procedure_in: ProcedureIn, current_user: User = Depends(check_is_admin_user), session: Session = Depends(get_db)):
    procedure: Procedure = Procedure.query(session).filter(Procedure.id == id).first()
    if not procedure:
        raise HTTPException(status_code=404, detail='route not found')

    procedure.program_id = procedure_in.program_id
    procedure.name = unidecode.unidecode(procedure_in.name).upper()
    procedure.objective = procedure_in.objective
    procedure.stimulus = procedure_in.stimulus
    procedure.answer = procedure_in.answer
    procedure.consequence = procedure_in.consequence
    procedure.material = procedure_in.material
    procedure.type_help = procedure_in.type_help
    procedure.attempts = procedure_in.attempts
    procedure.goal_value = procedure_in.goal_value
    procedure.description = procedure_in.description
    
    session.add(procedure)
    session.commit()

    return ProcedureOut.from_orm(procedure)
    

@router.delete('/{id}', summary='Delete procedure', response_model=List[ProcedureOut], tags=[tags])
async def delete(id: UUID, current_user: User = Depends(check_is_admin_user), session: Session = Depends(get_db)):
    pass