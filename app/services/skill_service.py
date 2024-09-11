from typing import List
from uuid import UUID
from app.constants.exceptions.skill_excepetions import SkillNotFoundError
from app.repositories.skill_repository import SkillRepository
from app.schemas.procedure_schemas import ProcedureSchemaIn, ProcedureSchemaOut
from app.schemas.skill_schemas import SkillManyIDs, SkillSchemaIn, SkillSchemaOut
from app.services.procedure_service import ProcedureService


class SkillService:
    def __init__(self, skill_repository: SkillRepository, procedure_service: ProcedureService):
        self.skill_repository = skill_repository
        self.procedure_service = procedure_service

    def create(self, skill_in: SkillSchemaIn) -> SkillSchemaOut:
        return self.skill_repository.create(skill_in)

    def get_id(self, id: UUID) -> SkillSchemaOut:
        return self.skill_repository.get_id(id)

    def get_all(self) -> List[SkillSchemaOut]:
        return self.skill_repository.get_all()

    def get_speciality(self, id: UUID) -> List[SkillSchemaOut]:
        return self.skill_repository.get_speciality(id)

    def update(self, id: UUID, skill_in: SkillSchemaIn) -> SkillSchemaOut:
        skill = self.skill_repository.get_id(id)
        if not skill:
            raise ValueError(SkillNotFoundError.MESSAGE)

        return self.skill_repository.update(skill, skill_in)

    def get_student(self, student_id: UUID) -> List[ProcedureSchemaOut]:
        uniques = self.procedure_service.get_unique_procedure(student_id)
        skill_ids = [result[0] for result in uniques]

        return self.skill_repository.get_skill_student(skill_ids)

    def get_procedures(self, id: UUID) -> List[ProcedureSchemaOut]:
        return self.procedure_service.get_all(id)

    def get_for_many_skills(self, skills_in: SkillManyIDs) -> List[ProcedureSchemaOut]:
        return self.procedure_service.get_for_many_skills(skills_in.skills)

    def create_procedure(self, id: UUID, procedure_in: ProcedureSchemaIn) -> ProcedureSchemaOut:
        return self.procedure_service.create(id, procedure_in)

    def update_procedure(self, procedure_id: UUID, procedure_in: ProcedureSchemaIn) -> ProcedureSchemaOut:
        return self.procedure_service.update(procedure_id, procedure_in)

    def get_procedure_id(self, procedure_id: UUID) -> ProcedureSchemaOut:
        return self.procedure_service.get_id(procedure_id)
