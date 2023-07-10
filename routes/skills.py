from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.security import check_is_admin_user
from db import get_db
from db.models import User, Instructor, Skill
from schemas.skill_schemas import SkillIn, SkillOut

router = APIRouter()

tags: str = "Skills"


@router.post('/', summary='Create skill', response_model=SkillOut, tags=[tags])
async def create(skill_in: SkillIn, current_user: User = Depends(check_is_admin_user), session: Session = Depends(get_db)):
    skill = Skill(
        company_id=current_user.company_id,
        name=skill_in.name,
        objective=skill_in.objective,
    )
    session.add(skill)
    session.commit()


@router.get('/', summary='Return skills list', response_model=List[SkillOut], tags=[tags])
async def get_all(current_user: User = Depends(check_is_admin_user), session: Session = Depends(get_db)):
    all_itens = Skill.query(session).all()
    return [SkillOut.from_orm(x) for x in all_itens]


@router.get('/{id}', summary='Return skill', tags=[tags])
async def get_id(id: UUID, current_user: User = Depends(check_is_admin_user), session: Session = Depends(get_db)):
    skill: Skill = Skill.query(
        session).filter(Instructor.id == id).first()
    if not skill:
        raise HTTPException(status_code=404, detail='route not found')

    return SkillOut.from_orm(skill)


@router.put('/{id}', summary='Update skill', tags=[tags], response_model=SkillOut)
async def update(id: UUID, skill_in: SkillIn, current_user: User = Depends(check_is_admin_user), session: Session = Depends(get_db)):
    skill: Skill = Skill.query(
        session).filter(Instructor.id == id).first()
    if not skill:
        raise HTTPException(status_code=404, detail='route not found')
    
    skill.name = skill_in.name,
    skill.objective = skill.objective

    session.add(skill)
    session.commit()

    return SkillOut.from_orm(skill)


@router.delete('/{id}', summary='Delete skill',  tags=[tags])
async def delete(id: UUID, current_user: User = Depends(check_is_admin_user), session: Session = Depends(get_db)):
    skill: Skill = Skill.query(
        session).filter(Instructor.id == id).first()
    if not skill:
        raise HTTPException(status_code=404, detail='route not found')
    session.delete(skill)
    session.commit()