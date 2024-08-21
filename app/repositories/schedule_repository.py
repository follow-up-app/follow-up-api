from typing import List
from uuid import UUID
from datetime import date, datetime
from sqlalchemy.orm import Session
from app.constants.enums.schedule_enum import ScheduleEnum
from app.schemas.instructor_schema import InstructorSchemaOut
from app.schemas.schedule_schemas import ScheduleSchemaEvent, ScheduleSchemaIn, ScheduleSchemaOut
from app.schemas.student_schemas import StudentSchemaOut
from db.models import Schedule, User
from sqlalchemy.sql.functions import func


class ScheduleRepository:
    def __init__(self, session: Session, current_user: User):
        self.session = session
        self.current_user = current_user

    def create(self,
               event_id: UUID,
               student: StudentSchemaOut,
               instructor: InstructorSchemaOut,
               date_schedule_in: datetime,
               date_schedule_out: datetime,
               schedule_in: ScheduleSchemaIn) -> ScheduleSchemaOut:

        schedule = Schedule(
            company_id=self.current_user.company_id,
            student_id=student.id,
            event_id=event_id,
            start=date_schedule_in,
            end=date_schedule_out,
            title=student.fullname + ' | ' + instructor.fullname,
            instructor_id=instructor.id,
            details=schedule_in.details,
            start_hour=schedule_in.start_hour,
            end_hour=schedule_in.end_hour,
            repeat=schedule_in.repeat,
            period=schedule_in.period,
            color=schedule_in.color,
            status=ScheduleEnum.SCHEDULED
        )

        self.session.add(schedule)
        self.session.commit()

        return schedule

    def get_id(self, id: UUID) -> ScheduleSchemaOut:
        return Schedule.query(self.session).filter(Schedule.id == id).first()

    def get_all(self) -> List[ScheduleSchemaOut]:
        return Schedule.query(self.session).filter(Schedule.company_id == self.current_user.company_id).all()

    def get_instructor(self, instructor_id: UUID) -> ScheduleSchemaOut:
        return Schedule.query(self.session).filter(Schedule.instructor_id == instructor_id).first()

    def get_scheduled(self):
        return Schedule.query(Session).filter(Schedule.company_id == self.current_user.company_id,
                                              Schedule.status == ScheduleEnum.SCHEDULED).all()

    def get_instructor_all(self, instructor_id: UUID) -> ScheduleSchemaOut:
        return Schedule.query(self.session).filter(Schedule.instructor_id == instructor_id).all()

    def get_event(self, event_id: UUID) -> List[ScheduleSchemaOut]:
        return Schedule.query(self.session).filter(Schedule.event_id == event_id).all()

    def done(self, schedule: Schedule) -> ScheduleSchemaOut:
        schedule.status = ScheduleEnum.DONE
        schedule.event_begin = datetime
        schedule.event_user_id = self.current_user.id

        self.session.add(schedule)
        self.session.commit()

        return schedule

    def student_arrival(self, schedule: Schedule) -> ScheduleSchemaOut:
        schedule.student_arrival = datetime.now()

        self.session.add(schedule)
        self.session.commit()

        return schedule

    def delete(self, id: UUID) -> bool:
        schedule = Schedule.query(self.session).filter(
            Schedule.id == id).first()

        self.session.delete(schedule)
        self.session.commit()

        return True

    def in_progress(self, schedule: Schedule) -> ScheduleSchemaOut:
        schedule.event_begin = datetime.now()
        schedule.event_user_id = self.current_user.id
        schedule.status = ScheduleEnum.IN_PROGRESS

        self.session.add(schedule)
        self.session.commit()

        return schedule

    def get_today(self, start_of_day: datetime, end_of_day: datetime) -> List[ScheduleSchemaOut]:
        return Schedule.query(self.session).filter(Schedule.start >= start_of_day,
                                                   Schedule.start <= end_of_day,
                                                   Schedule.status == ScheduleEnum.SCHEDULED).all()

    def get_student(self, student_id: UUID) -> ScheduleSchemaOut:
        return Schedule.query(self.session).filter(Schedule.student_id == student_id).first()

    def get_avalible_instructor(self, instructor_id: UUID) -> List[ScheduleSchemaOut]:
        return self.session.query(func.date(Schedule.start)).filter(
            Schedule.instructor_id == instructor_id, Schedule.status.in_(
                [ScheduleEnum.SCHEDULED, ScheduleEnum.IN_PROGRESS, ScheduleEnum.PAUSED])
        ).group_by(func.date(Schedule.start)).order_by(func.date(Schedule.start)).all()

    def get_schedule_instructor(self, instructor_id: UUID, start: date) -> List[ScheduleSchemaOut]:
        return Schedule.query(self.session).filter(
            Schedule.instructor_id == instructor_id,
            Schedule.status.in_(
                [ScheduleEnum.SCHEDULED, ScheduleEnum.IN_PROGRESS, ScheduleEnum.PAUSED]),
            func.date(Schedule.start) == start
        ).order_by(Schedule.start.asc()).all()

    def check_instructor(self, instructor_id: UUID, date_schedule_in: datetime, date_schedule_out: datetime) -> ScheduleSchemaOut:
        return Schedule.query(self.session).filter(
            Schedule.instructor_id == instructor_id,
            ((date_schedule_in >= Schedule.start) & (date_schedule_in < Schedule.end)) | (
                (date_schedule_out > Schedule.start) & (date_schedule_out <= Schedule.end))).first()

    def check_student(self, student_id: UUID, date_schedule_in: datetime, date_schedule_out: datetime) -> ScheduleSchemaOut:
        return Schedule.query(self.session).filter(
            Schedule.student_id == student_id,
            ((date_schedule_in >= Schedule.start) & (date_schedule_in < Schedule.end)) | (
                (date_schedule_out > Schedule.start) & (date_schedule_out <= Schedule.end))).first()

    def get_follow_up(self) -> List[ScheduleSchemaOut]:
        return Schedule.query(self.session).filter(Schedule.company_id == self.current_user.company_id).order_by(
            Schedule.updated_at.desc()).all()

    def get_date_filter(self, start: datetime, end: datetime, student_id: UUID) -> List[ScheduleSchemaOut]:
        schedules = Schedule.query(self.session).filter(
            Schedule.company_id == self.current_user.company_id,

            Schedule.start >= start,
            Schedule.start <= end).order_by(Schedule.start.asc()).all()

        if student_id is not None:
            schedules = schedules.filter(Schedule.student_id)

        return schedules
