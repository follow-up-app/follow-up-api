from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.security import check_is_admin_user
from db import get_db
from db.models import User, Instructor, Skill, Procedure
from schemas.skill_schemas import SkillIn, SkillOut
from schemas.procedure_schemas import ProcedureOut
import logging
from sqlalchemy.sql.functions import func

router = APIRouter()

tags: str = "Skills"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@router.post('/', summary='Create skill', response_model=SkillOut, tags=[tags])
async def create(skill_in: SkillIn, current_user: User = Depends(check_is_admin_user), session: Session = Depends(get_db)):
    try:
        skill = Skill(
            company_id=current_user.company_id,
            name=skill_in.name,
            objective=skill_in.objective,
        )
        session.add(skill)
        session.commit()

        return SkillOut.from_orm(skill)

    except Exception as e:
        logger.error(f"Error in create skill: {e}")
        raise HTTPException(status_code=500, detail='Server error')


@router.get('/', summary='Return skills list', response_model=List[SkillOut], tags=[tags])
async def get_all(current_user: User = Depends(check_is_admin_user), session: Session = Depends(get_db)):
    all_itens = Skill.query(session).all()
    return [SkillOut.from_orm(x) for x in all_itens]


@router.get('/{id}', summary='Return skill', tags=[tags])
async def get_id(id: UUID, current_user: User = Depends(check_is_admin_user), session: Session = Depends(get_db)):
    skill: Skill = Skill.query(
        session).filter(Skill.id == id).first()
    if not skill:
        raise HTTPException(status_code=404, detail='route not found')

    return SkillOut.from_orm(skill)


@router.get('/{id}/procedures', summary='Return list procedure reference skill', tags=[tags])
async def get_id(id: UUID, current_user: User = Depends(check_is_admin_user), session: Session = Depends(get_db)):
    all_itens: Procedure = Procedure.query(
        session).filter(Procedure.skill_id == id).all()
    return [ProcedureOut.from_orm(x) for x in all_itens]


@router.put('/{id}', summary='Update skill', tags=[tags], response_model=SkillOut)
async def update(id: UUID, skill_in: SkillIn, current_user: User = Depends(check_is_admin_user), session: Session = Depends(get_db)):
    skill: Skill = Skill.query(
        session).filter(Skill.id == id).first()
    if not skill:
        raise HTTPException(status_code=404, detail='route not found')

    try:
        skill.name = skill_in.name,
        skill.objective = skill.objective
        
        session.add(skill)
        session.commit()

        return SkillOut.from_orm(skill)
    except Exception as e:
        logger.error(f"Error in update skill: {e}")
        raise HTTPException(status_code=500, detail='Server error')


@router.delete('/{id}', summary='Delete skill',  tags=[tags])
async def delete(id: UUID, current_user: User = Depends(check_is_admin_user), session: Session = Depends(get_db)):
    skill: Skill = Skill.query(
        session).filter(Instructor.id == id).first()
    if not skill:
        raise HTTPException(status_code=404, detail='route not found')
    session.delete(skill)
    session.commit()


@router.get('/student/{student_id}', summary='Return skill list for student', tags=[tags])
async def get_id(student_id: UUID, session: Session = Depends(get_db)):
    unique_skills = session.query(Procedure.skill_id).filter(Procedure.student_id == student_id).distinct().all()
    skill_ids = [result[0] for result in unique_skills]
    skills: Skill = Skill.query(session).filter(Skill.id.in_(skill_ids)).all()

    return [SkillOut.from_orm(x) for x in skills]