from typing import List
from uuid import UUID
from app.constants.exceptions.contractor_exceptions import ContractorNotFoundError
from app.repositories.contractor_repository import ContractorRepository
from app.schemas.contractor_schemas import ContractorIn, ContractorOut


class ContractorService:
    def __init__(self, contractor_repository: ContractorRepository):
        self.contractor_repository = contractor_repository

    def create(self) -> ContractorOut:
        return self.contractor_repository.create()

    def get_all(self) -> List[ContractorOut]:
        return self.contractor_repository.get_all()

    def get_id(self, id: UUID) -> ContractorOut:
        return self.contractor_repository.get_id(id)

    def update(self, id: UUID, contractor_in: ContractorIn) -> ContractorOut:
        contractor = self.contractor_repository.get_id(id)
        if not contractor:
            raise ValueError(ContractorNotFoundError.MESSAGE)

        return self.student_repository.update(contractor, contractor_in)

    def company_contractors(self) ->List[ContractorOut]:
        contracts_ = self.contractor_repository.get_all()
        contracts = []
        for contract in contracts_:
            contracts.append(contract.id)

        return contracts
