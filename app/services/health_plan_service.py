from app.repositories.health_plan_repository import HealthPlanRepository
from app.schemas.health_plan_schemas import HealthPlanSchemaIn, HealthPlanSchemaOut
from uuid import UUID
from typing import List
from app.constants.exceptions.health_paln_exceptions import HealthPlanNotFoundError, HealthPlanExistsError


class HealthPlanService:
    def __init__(self,
                 health_plan_repository: HealthPlanRepository):
        self.health_plan_repository = health_plan_repository

    def create(self, health_plan_in: HealthPlanSchemaIn) -> HealthPlanSchemaOut:
        self.valid_document_exists(health_plan_in.document)

        return self.health_plan_repository.create(health_plan_in)

    def get_id(self, id: UUID) -> HealthPlanSchemaOut:
        return self.health_plan_repository.get_id(id)

    def get_all(self) -> List[HealthPlanSchemaOut]:
        return self.health_plan_repository.get_all()

    def update(self, id: UUID, health_plan_in: HealthPlanSchemaIn) -> HealthPlanSchemaOut:
        plan = self.health_plan_repository.get_id(id)
        if not plan:
            raise ValueError(HealthPlanNotFoundError.MESSAGE)

        self.valid_document_exists(health_plan_in.document)

        return self.health_plan_repository.update(plan, health_plan_in)

    def remove(self, id: UUID) -> bool:
        return self.health_plan_repository.remove(id)

    def valid_document_exists(self, document: str) -> bool:
        plan = self.health_plan_repository.get_document(document)
        if plan:
            raise ValueError(HealthPlanExistsError.MESSAGE)

        return True
