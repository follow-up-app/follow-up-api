from typing import List
from uuid import UUID
from app.constants.exceptions.address_exceptions import AddressNotFoundError
from app.repositories.address_contract_repository import AndressContractRepository
from app.schemas.address_contract_schemas import AddressContractorSchemaIn, AddressContractorSchemaOut


class AddressContractService:
    def __init__(self, address_contract_repository: AndressContractRepository):
        self.address_contract_repository = address_contract_repository

    def create(self, address_in: AddressContractorSchemaIn, contractor_id: UUID) -> AddressContractorSchemaOut:
        return self.address_contract_repository.create(address_in, contractor_id)

    def get_all(self) -> List[AddressContractorSchemaOut]:
        return self.address_contract_repository.get_all()

    def get_id(self, id: UUID) -> AddressContractorSchemaOut:
        return self.address_contract_repository.get_id(id)

    def get_contractor_id(self, contractor_id: UUID) -> AddressContractorSchemaOut:
        return self.address_contract_repository.get_contractor_id(contractor_id)

    def update(self, id: UUID, address_in: AddressContractorSchemaIn) -> AddressContractorSchemaOut:
        address = self.address_contract_repository.get_id(id)
        if not address:
            raise ValueError(AddressNotFoundError.MESSAGE)

        return self.address_contract_repository.update(address, address_in)

    def remove(self, id: UUID) -> bool:
        return self.address_contract_repository.remove(id)
