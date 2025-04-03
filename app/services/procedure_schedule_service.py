from typing import List
from uuid import UUID
from app.constants.exceptions.procedure_exceptions import ProcedureNotFoundError
from app.repositories.procedure_schedule_repository import ProcedureScheduleRepository
from app.schemas.procedure_schemas import ProcedureSchemaIn, ProcedureSchemaOut


class ProcedureScheduleService:
    def __init__(self, procedure_schedule_repository: ProcedureScheduleRepository):
        self.procedure_schedule_repository = procedure_schedule_repository

    def create(self, schedule_id: UUID, student_id: UUID,  procedure_in: ProcedureSchemaOut) -> ProcedureSchemaOut:
        return self.procedure_schedule_repository.create(schedule_id, student_id, procedure_in)

    def get_id(self, id: UUID) -> ProcedureSchemaOut:
        return self.procedure_schedule_repository.get_id(id)

    def get_all(self, skill_id: UUID) -> List[ProcedureSchemaOut]:
        return self.procedure_schedule_repository.get_all(skill_id)

    def get_schedule_all(self, schedule_id: UUID) -> List[ProcedureSchemaOut]:
        return self.procedure_schedule_repository.get_schedule_all(schedule_id)

    def get_schedule_student_skill(self, schedule_id: UUID, student_id: UUID, skill_id: UUID) -> List[ProcedureSchemaOut]:
        return self.procedure_schedule_repository.get_schedule_student_skill(schedule_id, student_id, skill_id)

    def get_student_procedure(self, student_id: UUID, procedure_id: UUID) -> List[ProcedureSchemaOut]:
        return self.procedure_schedule_repository.get_student_procedure(student_id, procedure_id)

    def get_schedule_skill(self, schedule_id: UUID, skill_id: UUID) -> List[ProcedureSchemaOut]:
        return self.procedure_schedule_repository.get_schedule_skill(schedule_id, skill_id)

    def update(self, id: UUID, procedure_in: ProcedureSchemaIn) -> ProcedureSchemaOut:
        procedure = self.procedure_schedule_repository.get_id(id)
        if not procedure:
            raise ValueError(ProcedureNotFoundError.MESSAGE)

        return self.procedure_schedule_repository.update(procedure, procedure_in)

    def delete(self, id: UUID) -> bool:
        return self.procedure_schedule_repository.delete(id)

    def check_procedure_schedule_student(self, schedule_id: UUID, student_id: UUID, procedure_id: UUID) -> ProcedureSchemaOut:
        return self.procedure_schedule_repository.check_procedure_schedule_student(schedule_id, student_id, procedure_id)

    def get_skill_procedures(self, skill_id: UUID, student_id: UUID) -> List[ProcedureSchemaOut]:
        return self.procedure_schedule_repository.get_skill_procedures(skill_id, student_id)
    
    def get_distinct_skill_procedure(self, skill_id: UUID, schedule_id: UUID) -> List[ProcedureSchemaOut]:
        return self.procedure_schedule_repository.get_distinct_skill_procedure(skill_id, schedule_id)

