from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.security import get_current_user
from app.repositories.procedure_repository import ProcedureRepository
from app.repositories.skill_repository import SkillRepository
from app.services.procedure_service import ProcedureService
from app.services.skill_service import SkillService
from db import get_db
from db.models import User
from app.schemas.skill_schemas import SkillManyIDs, SkillSchemaIn, SkillSchemaOut
from app.schemas.procedure_schemas import ProcedureSchemaIn, ProcedureSchemaOut
import logging

router = APIRouter()

tags: str = "Skills"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_service(session: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    procedure_repository = ProcedureRepository(session)
    procedure_service = ProcedureService(procedure_repository)

    skill_repository = SkillRepository(session, current_user)
    return SkillService(skill_repository, procedure_service)


@router.post('/', summary='create skill', response_model=SkillSchemaOut, tags=[tags])
async def create(skill_in: SkillSchemaIn, skill_service: SkillService = Depends(get_service)):
    try:
        skill = skill_service.create(skill_in)
        return SkillSchemaOut.from_orm(skill)

    except Exception as e:
        logger.error(f"Error in create skill: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.get('/', summary='Returns skills list', response_model=List[SkillSchemaOut], tags=[tags])
async def get_all(skill_service: SkillService = Depends(get_service)):
    try:
        skills = skill_service.get_all()
        return [SkillSchemaOut.from_orm(x) for x in skills]

    except Exception as e:
        logger.error(f"Error in query skills: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.get('/{id}', summary='Returns skill for id', response_model=SkillSchemaOut, tags=[tags])
async def get_id(id: UUID, skill_service: SkillService = Depends(get_service)):
    try:
        skill = skill_service.get_id(id)
        return SkillSchemaOut.from_orm(skill)

    except Exception as e:
        logger.error(f"Error in query skill for id: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.get('/specialty/{specialty_id}', summary='Returns skills list', response_model=List[SkillSchemaOut], tags=[tags])
async def get_speciality(specialty_id: UUID, skill_service: SkillService = Depends(get_service)):
    try:
        skills = skill_service.get_speciality(specialty_id)
        return [SkillSchemaOut.from_orm(x) for x in skills]

    except Exception as e:
        logger.error(f"Error in query skills: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.patch('/{id}', summary='Update skill', response_model=SkillSchemaOut, tags=[tags])
async def update(id: UUID, skill_in: SkillSchemaIn, skill_service: SkillService = Depends(get_service)):
    try:
        skill = skill_service.update(id, skill_in)
        return SkillSchemaOut.from_orm(skill)

    except Exception as e:
        logger.error(f"Error in update skill: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.get('/{id}/procedures', summary='Return list procedure reference skill', response_model=List[ProcedureSchemaOut], tags=[tags])
async def get_procedures(id: UUID, skill_service: SkillService = Depends(get_service)):
    try:
        procedures = skill_service.get_procedures(id)
        return [ProcedureSchemaOut.from_orm(x) for x in procedures]

    except Exception as e:
        logger.error(f"Error in procedure list: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.post('/many-procedures/', summary='Return list procedure reference skill', response_model=List[ProcedureSchemaOut], tags=[tags])
async def get_for_many_skills(skills_in: SkillManyIDs, skill_service: SkillService = Depends(get_service)):
    try:
        procedures = skill_service.get_for_many_skills(skills_in)
        return [ProcedureSchemaOut.from_orm(x) for x in procedures]

    except Exception as e:
        logger.error(f"Error in procedure list: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.post('/{id}/procedures', summary='Create procedure', response_model=ProcedureSchemaOut, tags=[tags])
async def create_procedure(id: UUID, procedure_in: ProcedureSchemaIn, skill_service: SkillService = Depends(get_service)):
    try:
        procedure = skill_service.create_procedure(id, procedure_in)
        return ProcedureSchemaOut.from_orm(procedure)

    except Exception as e:
        logger.error(f"Error in create procedure: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.patch('/procedures/{procedure_id}', summary='Update procedure', response_model=ProcedureSchemaOut, tags=[tags])
async def update_procedure(procedure_id: UUID, procedure_in: ProcedureSchemaIn, skill_service: SkillService = Depends(get_service)):
    try:
        procedure = skill_service.update_procedure(procedure_id, procedure_in)
        return ProcedureSchemaOut.from_orm(procedure)

    except Exception as e:
        logger.error(f"Error in update procedure: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.get('/procedures/{procedure_id}', summary='Create procedure', response_model=ProcedureSchemaOut, tags=[tags])
async def get_procedure_id(procedure_id: UUID, skill_service: SkillService = Depends(get_service)):
    try:
        procedure = skill_service.get_procedure_id(procedure_id)
        return ProcedureSchemaOut.from_orm(procedure)

    except Exception as e:
        logger.error(f"Error in query procedure: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.get('/student/{student_id}', summary='Return skill list for student', response_model=List[SkillSchemaOut], tags=[tags])
async def get_id(student_id: UUID, skill_service: SkillService = Depends(get_service)):
    try:
        skills = skill_service.get_student(student_id)
        return [SkillSchemaOut.from_orm(x) for x in skills]

    except Exception as e:
        logger.error(f"Error in skills student list: {e}")
        raise HTTPException(status_code=400, detail=str(e))
