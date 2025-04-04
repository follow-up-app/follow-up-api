from typing import List
from uuid import UUID
from sqlalchemy.orm import Session
from app.schemas.schedule_schemas import SkillScheduleSchemaOut, EventSkillOut
from db.models import SkillsSchedule, Schedule
from sqlalchemy.sql.functions import func


class SkillScheduleRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, scheduele_id: UUID, skill_id: UUID) -> SkillScheduleSchemaOut:
        skill_schedule = SkillsSchedule(
            schedule_id=scheduele_id,
            skill_id=skill_id,
        )
        self.session.add(skill_schedule)
        self.session.commit()

        return skill_schedule

    def get_id(self, id: UUID) -> SkillScheduleSchemaOut:
        return SkillsSchedule.query(self.session).filter(SkillsSchedule.id == id).first()

    def get_schedule(self, schedule_id: UUID) -> List[SkillScheduleSchemaOut]:
        return SkillsSchedule.query(self.session).filter(SkillsSchedule.schedule_id == schedule_id).distinct(SkillsSchedule.skill_id).all()

    def delete(self, id: UUID) -> bool:
        skill = SkillsSchedule.query(self.session).filter(
            SkillsSchedule.id == id).first()

        self.session.delete(skill)
        self.session.commit()

        return True

    def check_skill_schedule(self, schedule_id: UUID, skill_id: UUID) -> SkillScheduleSchemaOut:
        return SkillsSchedule.query(self.session).filter(
            SkillsSchedule.schedule_id == schedule_id,
            SkillsSchedule.skill_id == skill_id,
        ).first()

    def all_skill_schedules_events(self, event_id: UUID, skill_id: UUID) -> List[SkillScheduleSchemaOut]:
        return SkillsSchedule.query(self.session).filter(
            SkillsSchedule.event_id == event_id,
            SkillsSchedule.skill_id == skill_id
        ).all()

    def skills_for_event(self, event_id: UUID):
        return (self.session.query(func.count(SkillsSchedule.id))
        .filter(SkillsSchedule.event_id == event_id)
        .scalar())

    def all_skill_schedules_for_event(self, event_id: UUID) -> List[EventSkillOut]:
        results = SkillsSchedule.query(self.session).join(SkillsSchedule.schedule).filter(
            SkillsSchedule.event_id == event_id,
        ).distinct(SkillsSchedule.skill_id, Schedule.week_days).all()

        return [EventSkillOut.from_orm(item) for item in results]