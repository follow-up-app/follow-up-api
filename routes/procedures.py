from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.security import check_is_admin_user
from db import get_db
from db.models import Procedure, User, Student, Skill
from schemas.procedure_schemas import ProcedureIn, ProcedureOut
import logging

router = APIRouter()

tags: str = "Procedure"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@router.post('/', summary='Create procedure', tags=[tags], response_model=ProcedureOut)
async def create(procedure_in: ProcedureIn, current_user: User = Depends(check_is_admin_user), session: Session = Depends(get_db)):
    skill: Skill = Skill.query(session).filter(
        Skill.id == procedure_in.skill_id
    ).first()
    if not skill:
        raise HTTPException(status_code=404, detail='skill not found')

    try:
        procedure = Procedure(
            skill_id=procedure_in.skill_id,
            tries=procedure_in.tries,
            goal=procedure_in.goal,
            period=procedure_in.period,
            name=procedure_in.name,
            objective=procedure_in.objective,
            stimulus=procedure_in.stimulus,
            answer=procedure_in.answer,
            consequence=procedure_in.consequence,
            materials=procedure_in.materials,
            help=procedure_in.help,
        )
        session.add(procedure)
        session.commit()

        return ProcedureOut.from_orm(procedure)

    except Exception as e:
        logger.error(f"Error in create procedure: {e}")
        raise HTTPException(status_code=500, detail='Server error')


@router.get('/', summary='Returns procedures list', response_model=List[ProcedureOut], tags=[tags])
async def get_all(current_user: User = Depends(check_is_admin_user), session: Session = Depends(get_db)):
    all_itens = Procedure.query(session).all()
    return [ProcedureOut.from_orm(x) for x in all_itens]


@router.get('{id}/skills', summary='Returns procedures list in skill reference', response_model=List[ProcedureOut], tags=[tags])
async def get_all_program(id: UUID, current_user: User = Depends(check_is_admin_user), session: Session = Depends(get_db)):
    all_itens = Procedure.query(session).filter(Procedure.skill_id == id).all()
    return [ProcedureOut.from_orm(x) for x in all_itens]


@router.get('/{id}', summary='Returns procedure', tags=[tags], response_model=ProcedureOut)
async def get_id(id: UUID, current_user: User = Depends(check_is_admin_user), session: Session = Depends(get_db)):
    procedure: Procedure = Procedure.query(
        session).filter(Procedure.id == id).first()
    if not procedure:
        raise HTTPException(status_code=404, detail='route not found')

    return ProcedureOut.from_orm(procedure)


@router.put('/{id}', summary='Update procedure', tags=[tags], response_model=ProcedureOut)
async def update(id: UUID, procedure_in: ProcedureIn, current_user: User = Depends(check_is_admin_user), session: Session = Depends(get_db)):
    procedure: Procedure = Procedure.query(
        session).filter(Procedure.id == id).first()
    if not procedure:
        raise HTTPException(status_code=404, detail='route not found')
    
    try:
        procedure.skill_id = procedure_in.skill_id
        procedure.tries = procedure_in.tries
        procedure.name = procedure_in.name
        procedure.objective = procedure_in.objective
        procedure.stimulus = procedure_in.stimulus
        procedure.answer = procedure_in.answer
        procedure.consequence = procedure_in.consequence
        procedure.materials = procedure_in.materials
        procedure.help = procedure_in.help

        session.add(procedure)
        session.commit()

        return ProcedureOut.from_orm(procedure)
    
    except Exception as e:
        logger.error(f"Error in procedure update: {e}")
        raise HTTPException(status_code=500, detail='Server error')


@router.delete('/{id}', summary='Delete procedure', tags=[tags])
async def delete(id: UUID, current_user: User = Depends(check_is_admin_user), session: Session = Depends(get_db)):
    procedure: Procedure = Procedure.query(
        session).filter(Procedure.id == id).first()
    if not procedure:
        raise HTTPException(status_code=404, detail='route not found')
    session.delete(procedure)
    session.commit()
