from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.security import check_is_admin_user, get_current_user
from db import get_db
from db.models import StatusSchedule, Student, User, Instructor, Schedule, EventRepeat, Execution, SkillsSchedule
from schemas.schedule_schemas import ScheduleIn, ScheduleOut, ScheduleEvent
from db.mongo import Mongo
from datetime import datetime, date
from sqlalchemy.sql.functions import func
from core.event import Event
import logging


router = APIRouter()

tags: str = "Schedule"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


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

    if schedule_in.repeat == EventRepeat.WEEK:
        event = Event()
        event.weeks(
            current_user=current_user,
            session=session,
            event=schedule_in,
            instructor=instructor,
            student=student)

    try:
        if schedule_in.repeat == EventRepeat.WEEK:
            event = Event()
            event.weeks(
                current_user=current_user,
                session=session,
                event=schedule_in,
                instructor=instructor,
                student=student)

        if schedule_in.repeat == EventRepeat.MOUTH:
            event = Event()
            event.mouths(
                current_user=current_user,
                session=session,
                event=schedule_in,
                instructor=instructor,
                student=student)

        if schedule_in.repeat == EventRepeat.NO:
            event = Event()
            event.unique(
                current_user=current_user,
                session=session,
                event=schedule_in,
                instructor=instructor,
                student=student)

        # save notifications
        # mongo = Mongo()
        # mongo.create_schedule_notitification(instructor.user_id, schedule.id)
        # mongo.create_event_admin(session, schedule.id)

        return {'status': 200, 'message': 'Events created'}

    except Exception as e:
        logger.error(f"Error in create schedule: {e}")
        raise HTTPException(status_code=e.status_code, detail=e.detail)


@router.get('/', summary='Return schedule list', tags=[tags])
async def get_all(current_user: User = Depends(get_current_user), session: Session = Depends(get_db)):
    schedules = Schedule.query(session).filter(
        Schedule.status == StatusSchedule.SCHEDULED).all()

    for schedule in schedules:
        skills: SkillsSchedule = SkillsSchedule.query(session).filter(
            SkillsSchedule.schedule_id == schedule.id
        ).all()
        schedule.skills = skills

    return [ScheduleOut.from_orm(x) for x in schedules]


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

    try:
        for schedule in schedules:
            executions: Execution = Execution.query(session).filter(
                Execution.schedule_id == schedule.id).first()
            if not executions:
                skills: SkillsSchedule = SkillsSchedule.query(session).filter(
                    SkillsSchedule.schedule_id == schedule.id).all()
                for skill in skills:
                    session.delete(skill)

                session.delete(schedule)
                session.commit()

        return {'status': 200, 'message': 'Events deleteds'}

    except Exception as e:
        logger.error(f"Error in delete schedule: {e}")
        raise HTTPException(status_code=500, detail='Server error')


@router.delete('/{id}', summary='Delete schedule', tags=[tags])
async def delete(id: UUID, current_user: User = Depends(check_is_admin_user), session: Session = Depends(get_db)):
    schedule: Schedule = Schedule.query(
        session).filter(Schedule.id == id).first()
    if not schedule:
        raise HTTPException(status_code=404, detail='schedule not found')
    try:
        skills: SkillsSchedule = SkillsSchedule.query(session).filter(
            SkillsSchedule.schedule_id == schedule.id).all()

        for skill in skills:
            session.delete(skill)

        session.delete(schedule)
        session.commit()

        return {'status': 200, 'message': 'Events deleteds'}

    except Exception as e:
        logger.error(f"Error in delete schedule: {e}")
        raise HTTPException(status_code=500, detail='Server error')


@router.put('/{id}/update/{skill_schedule_id}', summary='Update status schedule', tags=[tags])
async def update(id: UUID, skill_schedule_id: UUID, schedule_in: ScheduleEvent, current_user: User = Depends(get_current_user), session: Session = Depends(get_db)):
    schedule: Schedule = Schedule.query(
        session).filter(Schedule.id == id).first()
    if not schedule:
        raise HTTPException(status_code=404, detail='schedule not found')
    skill_schedule: SkillsSchedule = SkillsSchedule.query(session).filter(
        SkillsSchedule.schedule_id == id
    ).first()
    if not skill_schedule:
        raise HTTPException(status_code=404, detail='skill-schedule not found')
    try:
        if schedule_in.status == StatusSchedule.CANCELED or schedule_in.status == StatusSchedule.PAUSED or schedule_in.status == StatusSchedule.DID_NOT_ATTEND:
            schedule.status = schedule_in.status

        if schedule_in.status == StatusSchedule.IN_PROGRESS:
            schedule.status = schedule_in.status
            schedule.event_begin = datetime.utcnow()
            schedule.event_user_id = current_user.id

        if schedule_in.status == StatusSchedule.DONE:
            skills: SkillsSchedule = SkillsSchedule.query(session).filter(
                SkillsSchedule.schedule_id == schedule.id, SkillsSchedule.finished == None).all()

            if not skills:
                schedule.event_finish = datetime.utcnow()
                schedule.event_user_id = current_user.id
                schedule.status = schedule_in.status

            skill_schedule.finished = True

        schedule.status = schedule_in.status
        session.add(schedule)
        session.add(skill_schedule)
        session.commit()

        return ScheduleOut.from_orm(schedule)

    except Exception as e:
        logger.error(f"Error in update schedule: {e}")
        raise HTTPException(status_code=500, detail='Server error')


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
        Schedule.instructor_id == instructor.id, Schedule.status.in_([StatusSchedule.SCHEDULED, StatusSchedule.IN_PROGRESS, StatusSchedule.PAUSED])
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
            skills: SkillsSchedule = SkillsSchedule.query(session).filter(
                SkillsSchedule.schedule_id == schd.id
            ).all()
            for skill in skills:
                lst = {
                    'id': schd.id,
                    'skill_schedule_id': skill.id,
                    'skill_name': skill.skill_name,
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


@router.get('/{id}/student-arrival', summary='Return schedule list', tags=[tags])
async def get_all(id: UUID, current_user: User = Depends(get_current_user), session: Session = Depends(get_db)):
    schedule: Schedule = Schedule.query(
        session).filter(Schedule.id == id).first()
    if not schedule:
        raise HTTPException(status_code=404, detail='schedule not found')

    try:
        schedule.student_arrival = datetime.utcnow()
        session.add(schedule)
        session.commit()

        return ScheduleOut.from_orm(schedule)

    except Exception as e:
        logger.error(f"Error in create schedule: {e}")
        raise HTTPException(status_code=e.status_code, detail=e.detail)
