from typing import List
from uuid import UUID
from app.repositories.skill_schedule_repository import SkillScheduleRepository
from app.schemas.schedule_schemas import SkillScheduleSchemaOut


class SkillScheduleService:
    def __init__(self, skill_schedule_repository: SkillScheduleRepository):
        self.skill_schedule_repository = skill_schedule_repository

    def create(self, scheduele_id: UUID, skill_id: UUID) -> SkillScheduleSchemaOut:
        return self.skill_schedule_repository.create(scheduele_id, skill_id)

    def get_id(self, id: UUID) -> SkillScheduleSchemaOut:
        return self.skill_schedule_repository.get_id(id)

    def get_schedule(self, schedule_id: UUID) -> List[SkillScheduleSchemaOut]:
        return self.skill_schedule_repository.get_schedule(schedule_id)

    def delete(self, id: UUID) -> bool:
        return self.skill_schedule_repository.delete(id)

    def check_skill_schedule(self, schedule_id: UUID, skill_id: UUID) -> SkillScheduleSchemaOut:
        return self.skill_schedule_repository.check_skill_schedule(schedule_id, skill_id)
