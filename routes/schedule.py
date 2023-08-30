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
from db.models import StatusSchedule, Student, User, Instructor, Schedule, Skill
from schemas.schedule_schemas import ScheduleIn, ScheduleOut

router = APIRouter()

tags: str = "Schedule"


@router.post('/', summary='Create schedule', response_model=ScheduleOut, tags=[tags])
async def create(schedule_in: ScheduleIn, current_user: User = Depends(check_is_admin_user), session: Session = Depends(get_db)):
    student: Student = Student.query(session).filter(
        Student.id == schedule_in.student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail='student not found')

    instructor: Instructor = Instructor.query(session).filter(
        Instructor.id == schedule_in.instructor_id).first()
    if not instructor:
        raise HTTPException(status_code=404, detail='instructor not found')

    skill: Skill = Skill.query(session).filter(
        Skill.id == schedule_in.skill_id).first()
    if not skill:
        raise HTTPException(status_code=404, detail='skill not found')

    schedule: Schedule = Schedule(
        company_id=current_user.company_id,
        skill_id=schedule_in.skill_id,
        student_id=schedule_in.student_id,
        start=schedule_in.start,
        end=schedule_in.end,
        title=schedule_in.title,
        instructor_id=schedule_in.instructor_id,
        details=schedule_in.details,
        status=StatusSchedule.SCHEDULED
    )
    session.add(schedule)
    session.commit()

    return ScheduleOut.from_orm(schedule)


@router.get('/', summary='Return schedule list', response_model=List[ScheduleOut], tags=[tags])
async def get_all(current_user: User = Depends(check_is_admin_user), session: Session = Depends(get_db)):
    all_itens = Schedule.query(session).all()
    return [ScheduleOut.from_orm(x) for x in all_itens]


@router.get('/{id}', summary='Return schedule', tags=[tags])
async def get_id(id: UUID, current_user: User = Depends(check_is_admin_user), session: Session = Depends(get_db)):
    schedule: Schedule = Schedule.query(session).filter(Schedule.id == id).first()
    if not schedule:
        raise HTTPException(status_code=404, detail='schedule not found')

    return ScheduleOut.from_orm(schedule)


@router.put('/{id}', summary='Update schedule', tags=[tags], response_model=ScheduleOut)
async def update(id: UUID, schedule_in: ScheduleIn, current_user: User = Depends(check_is_admin_user), session: Session = Depends(get_db)):
    schedule: Schedule = Schedule.query(session).filter(Schedule.id == id).first()
    if not schedule:
        raise HTTPException(status_code=404, detail='schedule not found')
    
    student: Student = Student.query(session).filter(
        Student.id == schedule_in.student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail='student not found')

    instructor: Instructor = Instructor.query(session).filter(
        Instructor.id == schedule_in.instructor_id).first()
    if not instructor:
        raise HTTPException(status_code=404, detail='instructor not found')

    skill: Skill = Skill.query(session).filter(
        Skill.id == schedule_in.skill_id).first()
    if not skill:
        raise HTTPException(status_code=404, detail='skill not found')
    

    schedule.title = schedule_in.title
    schedule.skill_id = schedule_in.skill_id
    schedule.instructor_id = schedule_in.instructor_id
    schedule.student_id = schedule_in.student_id
    schedule.start = schedule_in.start
    schedule.end = schedule_in.end
    schedule.details = schedule_in.details

    session.add(schedule)
    session.commit()

    return ScheduleOut.from_orm(schedule)

@router.delete('/{id}', summary='Delete schedule', tags=[tags])
async def delete(id: UUID, current_user: User = Depends(check_is_admin_user), session: Session = Depends(get_db)):
    schedule: Schedule = Schedule.query(session).filter(Schedule.id == id).first()
    if not schedule:
        raise HTTPException(status_code=404, detail='schedule not found')
    session.delete(schedule)
    session.commit()