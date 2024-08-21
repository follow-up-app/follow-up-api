from typing import List
from uuid import UUID
from app.constants.enums.permission_enum import PermissionEnum
from app.constants.enums.status_enum import StatusEnum
from app.constants.exceptions.instructor_exceptions import InstructorNotFoundError, InstructorUserCreateError
from app.repositories.instructor_repository import InstructorRepository
from app.schemas.address_instructor_schemas import AddressInstructorSchemaIn, AddressInstructorSchemaOut
from app.schemas.instructor_schema import InstructorSchemaIn, InstructorSchemaOut
from app.schemas.student_schemas import Filters
from app.schemas.user_schemas import UserSchemaIn, UserSchemaOut
from app.services.address_instructor_service import AddressInstructorService
from app.services.user_service import UserService


class InstructorService:
    def __init__(self,
                 instructor_repository: InstructorRepository,
                 user_service: UserService,
                 address_instructor_service: AddressInstructorService):
        self.instructor_repository = instructor_repository
        self.user_service = user_service
        self.address_instructor_service = address_instructor_service

    def create(self, instructor_in: InstructorSchemaIn) -> InstructorSchemaOut:
        user_schema = UserSchemaIn(
            fullname=instructor_in.fullname,
            email=instructor_in.email,
            permission=PermissionEnum.INSTRUCTOR,
            document=instructor_in.document,
            position='PROFISSIONAL',
        )
        user = self.user_service.create(user_schema)
        if not user:
            raise ValueError(InstructorUserCreateError.MESSAGE)

        return self.instructor_repository.create(user.id, instructor_in)

    def get_all(self) -> List[InstructorSchemaOut]:
        return self.instructor_repository.get_all()

    def get_id(self, id: UUID) -> InstructorSchemaOut:
        return self.instructor_repository.get_id(id)

    def get_actives_all(self):
        return self.instructor_repository.get_actives_all()

    def update_active(self, id: UUID) -> InstructorSchemaOut:
        instructor = self.instructor_repository.get_id(id)
        if not instructor:
            raise ValueError(InstructorNotFoundError.MESSAGE)

        self.user_service.update_active(instructor.user_id)

        if instructor.status == StatusEnum.ACTIVE:
            return self.instructor_repository.inactive(instructor)

        if instructor.status == StatusEnum.INACTIVE:
            return self.instructor_repository.active(instructor)

    def update(self, id: UUID, instructor_in: InstructorSchemaIn) -> InstructorSchemaOut:
        instructor = self.instructor_repository.get_id(id)
        if not instructor:
            raise ValueError(InstructorNotFoundError.MESSAGE)

        return self.instructor_repository.update(instructor, instructor_in)

    def save_avatar(self, id: UUID, file: bytes) -> UserSchemaOut:
        print(id)
        instructor = self.instructor_repository.get_id(id)
        if not instructor:
            raise ValueError(InstructorNotFoundError.MESSAGE)

        return self.user_service.save_avatar(instructor.user_id, file)

    def avatar(self, id: UUID):
        instructor = self.instructor_repository.get_id(id)
        if not instructor:
            raise ValueError(InstructorNotFoundError.MESSAGE)

        return instructor.avatar

    def get_instructor_user(self) -> InstructorSchemaOut:
        return self.instructor_repository.get_instructor_user()

    def create_address(self,  instructor_id: UUID, address_in: AddressInstructorSchemaIn) -> AddressInstructorSchemaOut:
        instructor = self.instructor_repository.get_id(instructor_id)
        if not instructor:
            raise ValueError(InstructorNotFoundError.MESSAGE)

        return self.address_instructor_service.create(address_in, instructor.id)

    def get_address(self, instructor_id: UUID) -> AddressInstructorSchemaOut:
        instructor = self.instructor_repository.get_id(instructor_id)
        if not instructor:
            raise ValueError(InstructorNotFoundError.MESSAGE)

        return self.address_instructor_service.get_instructor(instructor.id)

    def update_address(self, address_id: UUID, address_in: AddressInstructorSchemaIn) -> AddressInstructorSchemaOut:
        return self.address_instructor_service.update(address_id, address_in)

    def get_filters(self, filters_in: Filters) -> List[InstructorSchemaOut]:
        return self.instructor_repository.get_filters(filters_in)
