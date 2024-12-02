from typing import List
from uuid import UUID
from app.constants.enums.instructor_payments_enum import ModePaymentEnum, TypePaymentEnum
from app.constants.enums.permission_enum import PermissionEnum
from app.constants.enums.status_enum import StatusEnum
from app.constants.exceptions.instructor_exceptions import InstructorNotFoundError, InstructorUserCreateError
from app.repositories.address_instructor_repository import AddressInstructorRepository
from app.repositories.instructor_payment_repository import InstructorPaymentRepository
from app.repositories.instructor_repository import InstructorRepository
from app.schemas.address_instructor_schemas import AddressInstructorSchemaIn, AddressInstructorSchemaOut
from app.schemas.instructor_payment_schema import InstructorPaymentSchemaIn, InstructorPaymentSchemaOut
from app.schemas.instructor_schema import InstructorSchemaIn, InstructorSchemaOut
from app.schemas.student_schemas import Filters
from app.schemas.user_schemas import UserSchemaIn, UserSchemaOut
from app.services.user_service import UserService


class InstructorService:
    def __init__(self,
                 instructor_repository: InstructorRepository,
                 user_service: UserService,
                 address_instructor_repository: AddressInstructorRepository,
                 instructor_payment_repository: InstructorPaymentRepository):
        self.instructor_repository = instructor_repository
        self.user_service = user_service
        self.address_instructor_repository = address_instructor_repository
        self.instructor_payment_repository = instructor_payment_repository

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

        return self.address_instructor_repository.create(address_in, instructor.id)

    def get_address(self, instructor_id: UUID) -> AddressInstructorSchemaOut:
        instructor = self.instructor_repository.get_id(instructor_id)
        if not instructor:
            raise ValueError(InstructorNotFoundError.MESSAGE)

        return self.address_instructor_repository.get_instructor(instructor.id)

    def update_address(self, address_id: UUID, address_in: AddressInstructorSchemaIn) -> AddressInstructorSchemaOut:
        return self.address_instructor_repository.update(address_id, address_in)

    def get_filters(self, filters_in: Filters) -> List[InstructorSchemaOut]:
        return self.instructor_repository.get_filters(filters_in)

    def create_data_payment(self, instructor_id: UUID, instructor_payment_in: InstructorPaymentSchemaIn) -> InstructorSchemaOut:
        instructor = self.instructor_repository.get_id(instructor_id)
        if not instructor:
            raise ValueError(InstructorNotFoundError.MESSAGE)

        self.instructor_payment_repository.create_payment_details(
            instructor.id, instructor_payment_in)
        if instructor_payment_in.comission:
            instructor_payment_in.comission = instructor_payment_in.comission / 100

        return self.instructor_repository.update_type_payment(instructor, instructor_payment_in)

    def update_data_payment(self, instructor_id: UUID, instructor_payment_in: InstructorPaymentSchemaIn) -> InstructorSchemaOut:
        instructor = self.instructor_repository.get_id(instructor_id)
        if not instructor:
            raise ValueError(InstructorNotFoundError.MESSAGE)

        payment_details = self.instructor_payment_repository.get_payment_details(
            instructor.id)

        self.instructor_payment_repository.update_payment_details(
            payment_details, instructor_payment_in)

        if instructor_payment_in.comission:
            instructor_payment_in.comission = instructor_payment_in.comission / 100

        return self.instructor_repository.update_type_payment(instructor, instructor_payment_in)

    def get_data_payment(self, instructor_id: UUID) -> InstructorPaymentSchemaOut:
        instructor = self.instructor_repository.get_id(instructor_id)
        if not instructor:
            raise ValueError(InstructorNotFoundError.MESSAGE)
        return self.instructor_payment_repository.get_payment_details(instructor.id)
