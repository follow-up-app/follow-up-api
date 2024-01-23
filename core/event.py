from db.models import Schedule, Skill, Instructor, Student, StatusSchedule
from sqlalchemy.orm import Session
from schemas.schedule_schemas import ScheduleIn, ScheduleOut, ScheduleEvent
from fastapi import HTTPException
from datetime import datetime, date, timedelta
import uuid


class Event:
    @staticmethod
    def weeks(current_user, session: Session, event: ScheduleIn, instructor: Instructor, student: Student, skill: Skill):
        uuid.uuid4()
        days = event.period * 30
        max_date = event.schedule_in + timedelta(days=round(days))
        period_ = max_date - event.schedule_in
        period = round(period_.days / 7)
        events = []
        event_id = uuid.uuid4()
        for _ in range(period):
            date_i = f'{event.schedule_in} {event.start_hour}'
            date_schedule_in = datetime.strptime(date_i, '%Y-%m-%d %H:%M')

            date_o = f'{event.schedule_in} {event.end_hour}'
            date_schedule_out = datetime.strptime(date_o, '%Y-%m-%d %H:%M')

            if date_schedule_out <= date_schedule_in:
                raise HTTPException(
                    status_code=506, detail='A hora inicial deve ser menor que a hora final')

            title = student.fullname + ' - ' + skill.name

            instructor_e: Schedule = Schedule.query(session).filter(
                Schedule.instructor_id == instructor.id,
                ((date_schedule_in >= Schedule.start) & (date_schedule_in <= Schedule.end)) | (
                    (date_schedule_out >= Schedule.start) & (date_schedule_out <= Schedule.end))
            ).first()
            if instructor_e:
                raise HTTPException(
                    status_code=504, detail='Profissional não esta disponível para estas datas')

            student_e: Schedule = Schedule.query(session).filter(
                Schedule.student_id == student.id,
                ((date_schedule_in >= Schedule.start) & (date_schedule_in <= Schedule.end)) | (
                    (date_schedule_out >= Schedule.start) & (date_schedule_out <= Schedule.end))
            ).first()
            if student_e:
                raise HTTPException(
                    status_code=505, detail='Cliente não esta disponível para estas datas')

            schedule: Schedule = Schedule(
                company_id=current_user.company_id,
                skill_id=event.skill_id,
                student_id=event.student_id,
                event_id=event_id,
                start=date_schedule_in,
                end=date_schedule_out,
                title=title,
                instructor_id=event.instructor_id,
                details=event.details,
                start_hour=event.start_hour,
                end_hour=event.end_hour,
                repeat=event.repeat,
                period=event.period,
                color=event.color,
                status=StatusSchedule.SCHEDULED
            )
            events.append(schedule)
            event.schedule_in += timedelta(days=7)
        try:
            session.add_all(events)
            session.commit()
        except:
            raise HTTPException(status_code=500, detail="System error")

        return events

    @staticmethod
    def mouths(current_user, session: Session, event: ScheduleIn, instructor: Instructor, student: Student, skill: Skill):
        uuid.uuid4()
        event_id = uuid.uuid4()
        events = []

        for _ in range(event.period):
            date_i = f'{event.schedule_in} {event.start_hour}'
            date_schedule_in = datetime.strptime(date_i, '%Y-%m-%d %H:%M')

            date_o = f'{event.schedule_in} {event.end_hour}'
            date_schedule_out = datetime.strptime(date_o, '%Y-%m-%d %H:%M')

            if date_schedule_out <= date_schedule_in:
                raise HTTPException(
                    status_code=506, detail='A hora inicial deve ser menor que a hora final')

            title = student.fullname + ' - ' + skill.name

            instructor_e: Schedule = Schedule.query(session).filter(
                Schedule.instructor_id == instructor.id,
                ((date_schedule_in >= Schedule.start) & (date_schedule_in <= Schedule.end)) | (
                    (date_schedule_out >= Schedule.start) & (date_schedule_out <= Schedule.end))
            ).first()
            if instructor_e:
                raise HTTPException(
                    status_code=504, detail='Profissional não esta disponível para estas datas')

            student_e: Schedule = Schedule.query(session).filter(
                Schedule.student_id == student.id,
                ((date_schedule_in >= Schedule.start) & (date_schedule_in <= Schedule.end)) | (
                    (date_schedule_out >= Schedule.start) & (date_schedule_out <= Schedule.end))
            ).first()
            if student_e:
                raise HTTPException(
                    status_code=505, detail='Cliente não esta disponível para estas datas')

            schedule: Schedule = Schedule(
                company_id=current_user.company_id,
                skill_id=event.skill_id,
                student_id=event.student_id,
                event_id=event_id,
                start=date_schedule_in,
                end=date_schedule_out,
                title=title,
                instructor_id=event.instructor_id,
                details=event.details,
                start_hour=event.start_hour,
                end_hour=event.end_hour,
                repeat=event.repeat,
                period=event.period,
                color=event.color,
                status=StatusSchedule.SCHEDULED
            )
            events.append(schedule)
            event.schedule_in += timedelta(days=30)
        try:
            session.add_all(events)
            session.commit()
        except:
            raise HTTPException(status_code=500, detail="System error")

        return events

    @staticmethod
    def unique(current_user, session: Session, event: ScheduleIn, instructor: Instructor, student: Student, skill: Skill):
        uuid.uuid4()
        event_id = uuid.uuid4()
        events = []

        date_i = f'{event.schedule_in} {event.start_hour}'
        date_schedule_in = datetime.strptime(date_i, '%Y-%m-%d %H:%M')

        date_o = f'{event.schedule_in} {event.end_hour}'
        date_schedule_out = datetime.strptime(date_o, '%Y-%m-%d %H:%M')

        if date_schedule_out <= date_schedule_in:
            raise HTTPException(
                status_code=506, detail='A hora inicial deve ser menor que a hora final')

        title = student.fullname + ' - ' + skill.name

        instructor_e: Schedule = Schedule.query(session).filter(
            Schedule.instructor_id == instructor.id,
            Schedule.start == date_schedule_in
        ).first()
        if instructor_e:
            raise HTTPException(
                status_code=504, detail='Profissional não esta disponível para estas datas')

        student_e: Schedule = Schedule.query(session).filter(
            Schedule.student_id == student.id,
            Schedule.start == date_schedule_in
        ).first()

        if student_e:
            raise HTTPException(
                status_code=505, detail='Cliente não esta disponível para estas datas')

        schedule: Schedule = Schedule(
            company_id=current_user.company_id,
            skill_id=event.skill_id,
            student_id=event.student_id,
            event_id=event_id,
            start=date_schedule_in,
            end=date_schedule_out,
            title=title,
            instructor_id=event.instructor_id,
            details=event.details,
            start_hour=event.start_hour,
            end_hour=event.end_hour,
            repeat=event.repeat,
            period=event.period,
            color=event.color,
            status=StatusSchedule.SCHEDULED
        )
        events.append(schedule)
        try:
            session.add_all(events)
            session.commit()
        except:
            raise HTTPException(status_code=500, detail="System error")

        return events
