from typing import List
from uuid import UUID
from app.constants.exceptions.procedure_exceptions import ProcedureNotFoundError
from app.repositories.procedure_repository import ProcedureRepository
from app.schemas.procedure_schemas import ProcedureSchemaIn, ProcedureSchemaOut


class ProcedureService:
    def __init__(self, procedure_repository: ProcedureRepository):
        self.procedure_repository = procedure_repository

    def create(self, skill_id: UUID, procedure_in: ProcedureSchemaIn) -> ProcedureSchemaOut:
        return self.procedure_repository.create(skill_id, procedure_in)

    def get_id(self, id: UUID) -> ProcedureSchemaOut:
        return self.procedure_repository.get_id(id)

    def get_all(self, skill_id: UUID) -> List[ProcedureSchemaOut]:
        return self.procedure_repository.get_all(skill_id)
    
    def get_for_many_skills(self, skills: List[UUID]) -> List[ProcedureSchemaOut]:
        return self.procedure_repository.get_for_many_skills(skills)

    def update(self, id: UUID, procedure_in: ProcedureSchemaIn) -> ProcedureSchemaOut:
        procedure = self.procedure_repository.get_id(id)
        if not procedure:
            raise ValueError(ProcedureNotFoundError.MESSAGE)

        return self.procedure_repository.update(procedure, procedure_in)