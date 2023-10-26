from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status
from core.security import check_is_admin_user, get_current_user
from db import get_db
from db.models import StatusSchedule, Student, User, Instructor, Schedule, Skill
from schemas.schedule_schemas import ScheduleIn, ScheduleOut, ScheduleEvent
from db.mongo import Mongo
from datetime import datetime, date

router = APIRouter()

tags: str = "Schedule"


@router.post('/', summary='Create schedule', tags=[tags])
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
        start=schedule_in.schedule_in,
        end=schedule_in.schedule_out,
        title=schedule_in.title,
        instructor_id=schedule_in.instructor_id,
        details=schedule_in.details,
        status=StatusSchedule.SCHEDULED
    )
    session.add(schedule)
    session.commit()

    # save notifications
    mongo = Mongo()
    mongo.create_schedule_notitification(instructor.user_id, schedule.id)
    mongo.create_event_admin(session, schedule.id)

    return ScheduleOut.from_orm(schedule)


@router.get('/', summary='Return schedule list', response_model=List[ScheduleOut], tags=[tags])
async def get_all(current_user: User = Depends(get_current_user), session: Session = Depends(get_db)):
    all_itens = Schedule.query(session).all()
    return [ScheduleOut.from_orm(x) for x in all_itens]


@router.get('list/{instructor_id}', summary='Return schedule instructor', response_model=List[ScheduleOut], tags=[tags])
async def get_id(instructor_id: UUID, current_user: User = Depends(get_current_user), session: Session = Depends(get_db)):
    all_itens: Schedule = Schedule.query(
        session).filter(Schedule.instructor_id == instructor_id).all()
    return [ScheduleOut.from_orm(x) for x in all_itens]


@router.get('detail/{id}', summary='Return schedule', tags=[tags])
async def get_id(id: UUID, current_user: User = Depends(get_current_user), session: Session = Depends(get_db)):
    schedule: Schedule = Schedule.query(
        session).filter(Schedule.id == id).first()
    if not schedule:
        raise HTTPException(status_code=404, detail='schedule not found')

    return ScheduleOut.from_orm(schedule)


@router.put('/{id}', summary='Update schedule', tags=[tags], response_model=ScheduleOut)
async def update(id: UUID, schedule_in: ScheduleIn, current_user: User = Depends(check_is_admin_user), session: Session = Depends(get_db)):
    schedule: Schedule = Schedule.query(
        session).filter(Schedule.id == id).first()
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
    schedule.start = schedule_in.schedule_in
    schedule.end = schedule_in.schedule_out
    schedule.details = schedule_in.details

    session.add(schedule)
    session.commit()

    # save notifications
    mongo = Mongo()
    mongo.update_schedule_notitification(instructor.user_id, schedule.id)
    mongo.update_event_admin(session, schedule.id)

    return ScheduleOut.from_orm(schedule)


@router.delete('/{id}', summary='Delete schedule', tags=[tags])
async def delete(id: UUID, current_user: User = Depends(check_is_admin_user), session: Session = Depends(get_db)):
    schedule: Schedule = Schedule.query(
        session).filter(Schedule.id == id).first()
    if not schedule:
        raise HTTPException(status_code=404, detail='schedule not found')
    session.delete(schedule)
    session.commit()


@router.put('/{id}/update', summary='Update status schedule', tags=[tags])
async def update(id: UUID, schedule_in: ScheduleEvent, current_user: User = Depends(get_current_user), session: Session = Depends(get_db)):
    schedule: Schedule = Schedule.query(
        session).filter(Schedule.id == id).first()
    if not schedule:
        raise HTTPException(status_code=404, detail='schedule not found')

    if schedule_in.status == StatusSchedule.IN_PROGRESS:
        schedule.event_begin = datetime.utcnow()
        schedule.event_user_id = current_user.id

    if schedule_in.status == StatusSchedule.DONE:
        schedule.event_finish = datetime.utcnow()
        schedule.event_user_id = current_user.id

    schedule.status = schedule_in.status
    session.add(schedule)
    session.commit()

    return ScheduleOut.from_orm(schedule)


@router.get('/schedule-today', summary='Return all schedule today', response_model=List[ScheduleOut], tags=[tags])
async def get_today(current_user: User = Depends(get_current_user), session: Session = Depends(get_db)):
    today = date.today()
    start_of_day = datetime.combine(today, datetime.min.time())
    end_of_day = datetime.combine(today, datetime.max.time())

    all_itens: Schedule = Schedule.query(
        session).filter(Schedule.start >= start_of_day, Schedule.start <= end_of_day, Schedule.status == StatusSchedule.SCHEDULED).all()
    return [ScheduleOut.from_orm(x) for x in all_itens]
