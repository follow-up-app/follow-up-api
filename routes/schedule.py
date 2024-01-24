from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.security import check_is_admin_user, get_current_user
from db import get_db
from db.models import StatusSchedule, Student, User, Instructor, Schedule, Skill, EventRepeat, Execution
from schemas.schedule_schemas import ScheduleIn, ScheduleOut, ScheduleEvent
from db.mongo import Mongo
from datetime import datetime, date
from sqlalchemy.sql.functions import func
from core.event import Event


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

    if schedule_in.repeat == EventRepeat.WEEK:
        event = Event()
        event.weeks(
            current_user=current_user,
            session=session,
            event=schedule_in,
            instructor=instructor,
            student=student,
            skill=skill)

    if schedule_in.repeat == EventRepeat.MOUTH:
        event = Event()
        event.mouths(
            current_user=current_user,
            session=session,
            event=schedule_in,
            instructor=instructor,
            student=student,
            skill=skill)

    if schedule_in.repeat == EventRepeat.NO:
        event = Event()
        event.unique(
            current_user=current_user,
            session=session,
            event=schedule_in,
            instructor=instructor,
            student=student,
            skill=skill)

    # save notifications
    # mongo = Mongo()
    # mongo.create_schedule_notitification(instructor.user_id, schedule.id)
    # mongo.create_event_admin(session, schedule.id)

    return {'status': 200, 'message': 'Events created'}


@router.get('/', summary='Return schedule list', response_model=List[ScheduleOut], tags=[tags])
async def get_all(current_user: User = Depends(get_current_user), session: Session = Depends(get_db)):
    all_itens = Schedule.query(session).filter(
        Schedule.status == StatusSchedule.SCHEDULED).all()
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


@router.delete('/events/{event_id}', summary='Remove all schedules', tags=[tags])
async def delete_all(event_id: UUID, current_user: User = Depends(check_is_admin_user), session: Session = Depends(get_db)):
    schedules: Schedule = Schedule.query(
        session).filter(Schedule.event_id == event_id).all()
    if not schedules:
        raise HTTPException(status_code=404, detail='schedule not found')

    for schedule in schedules:
        executions: Execution = Execution.query(session).filter(
            Execution.schedule_id == schedule.id).first()
        if not executions:
            session.delete(schedule)
            session.commit()

    return {'status': 200, 'message': 'Events deleteds'}


@router.delete('/{id}', summary='Delete schedule', tags=[tags])
async def delete(id: UUID, current_user: User = Depends(check_is_admin_user), session: Session = Depends(get_db)):
    schedule: Schedule = Schedule.query(
        session).filter(Schedule.id == id).first()
    if not schedule:
        raise HTTPException(status_code=404, detail='schedule not found')
    session.delete(schedule)
    session.commit()

    return {'status': 200, 'message': 'Events deleteds'}


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


@router.get('/avalible-instructor', summary='Return schedule list', tags=[tags])
async def get_all(current_user: User = Depends(get_current_user), session: Session = Depends(get_db)):
    instructor: Instructor = Instructor.query(session).filter(
        Instructor.user_id == current_user.id).first()
    if not instructor:
        raise HTTPException(status_code=404, detail='instructor not found')

    stmt = session.query(func.date(Schedule.start)).filter(
        Schedule.instructor_id == instructor.id, Schedule.status == StatusSchedule.SCHEDULED
    ).group_by(func.date(Schedule.start)).order_by(func.date(Schedule.start)).all()

    response = {}
    for item in stmt:
        schedules: Schedule = Schedule.query(session).filter(
            Schedule.instructor_id == instructor.id,
            Schedule.status == StatusSchedule.SCHEDULED,
            func.date(Schedule.start) == item[0]
        ).order_by(Schedule.start.asc()).all()

        response[item[0]] = []

        for schd in schedules:
            lst = {
                'id': schd.id,
                'day': schd.start.day,
                'hour_start': schd.start.hour,
                'min_start': schd.start.minute,
                'hour_end': schd.end.hour,
                'min_end': schd.end.minute,
                'student': schd.student.id,
                'name': schd.student.fullname,
                'avatar': schd.student.avatar,
                'height': 80,
            }
            response[item[0]].append(lst)

    return response
