from typing import List
from uuid import UUID
from app.constants.exceptions.address_exceptions import AddressNotFoundError
from app.repositories.address_instructor_repository import AddressInstructorRepository
from app.schemas.address_instructor_schemas import AddressInstructorSchemaIn, AddressInstructorSchemaOut

class AddressInstructorService:
    def __init__(self, address_instructor_repository: AddressInstructorRepository):
        self.address_instructor_repository = address_instructor_repository

    def create(self, address_in: AddressInstructorSchemaIn, instructor_id: UUID) -> AddressInstructorSchemaOut:
        return self.address_instructor_repository.create(address_in, instructor_id)

    def get_all(self, instructor_id: UUID) -> List[AddressInstructorSchemaOut]:
        return self.address_instructor_repository.get_all(instructor_id)

    def get_id(self, id: UUID) -> AddressInstructorSchemaOut:
        return self.address_instructor_repository.get_id(id)
    
    def get_instructor(self, instructor_id: UUID) -> AddressInstructorSchemaOut:
        return self.address_instructor_repository.get_instructor(instructor_id)

    def update(self, id: UUID, address_in: AddressInstructorSchemaIn) -> AddressInstructorSchemaOut:
        address = self.address_instructor_repository.get_id(id)
        if not address:
            raise ValueError(AddressNotFoundError.MESSAGE)

        return self.address_instructor_repository.update(address, address_in)

    def remove(self, id: UUID) -> bool:
        return self.address_instructor_repository.remove(id)