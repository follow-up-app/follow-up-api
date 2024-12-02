from typing import List
from uuid import UUID
from app.constants.exceptions.responsible_contract_exceptions import ResponibleNotFoundError
from app.repositories.responsible_contract_repository import ResponsibleContractRepository
from app.schemas.responsible_contract_schemas import ResponsibleContractSchemaIn, ResponsibleContractSchemaOut


class ResponsibleContractService:
    def __init__(self, responsible_contract_repository: ResponsibleContractRepository):
        self.responsible_contract_repository = responsible_contract_repository

    def create(self, responsible_contract_in: ResponsibleContractSchemaIn, contractor_id: UUID) -> ResponsibleContractSchemaOut:
        return self.responsible_contract_repository.create(responsible_contract_in, contractor_id)

    def get_all(self) -> List[ResponsibleContractSchemaOut]:
        return self.responsible_contract_repository.get_all()

    def get_id(self, id: UUID) -> ResponsibleContractSchemaOut:
        return self.responsible_contract_repository.get_id(id)

    def get_contractor_id(self, contractor_id: UUID) -> List[ResponsibleContractSchemaOut]:
        return self.responsible_contract_repository.get_contractor_id(contractor_id)

    def update(self, id: UUID, responsible_contract_in: ResponsibleContractSchemaIn) -> ResponsibleContractSchemaOut:
        responsible = self.responsible_contract_repository.get_id(id)
        if not responsible:
            raise ValueError(ResponibleNotFoundError.MESSAGE)

        return self.responsible_contract_repository.update(responsible, responsible_contract_in)

    def remove(self, id: UUID) -> bool:
        return self.responsible_contract_repository.remove(id)
