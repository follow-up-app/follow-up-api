import os
from typing import List
from uuid import UUID
from app.constants.enums.status_enum import StatusEnum
from app.constants.exceptions.student_exceptions import StudentDocumentAlreadyExistsError, StudentNotFoundError, PlanExistsError
from app.repositories.student_repository import StudentRepository
from app.schemas.address_contract_schemas import AddressContractorSchemaIn, AddressContractorSchemaOut
from app.schemas.responsible_contract_schemas import ResponsibleContractSchemaIn, ResponsibleContractSchemaOut
from app.schemas.student_schemas import Filters, StudentSchemaIn, StudentSchemaOut, StudentPlanSchemaOut
from app.services.address_contract_service import AddressContractService
from app.services.contractor_service import ContractorService
from app.services.responsible_contract_service import ResponsibleContractService
from app.schemas.contractor_schemas import ContractorIn, ContractorOut

class StudentService:
    def __init__(self, student_repository: StudentRepository,
                 contractor_service: ContractorService,
                 responsible_contract_service: ResponsibleContractService,
                 address_contract_service: AddressContractService):
        self.student_repository = student_repository
        self.contractor_service = contractor_service
        self.responsible_contract_service = responsible_contract_service
        self.address_contract_service = address_contract_service

    def create(self, student_in: StudentSchemaIn) -> StudentSchemaOut:
        # check_document = self.student_repository.get_document(
        #     student_in.document)
        # if check_document:
        #     raise ValueError(StudentDocumentAlreadyExistsError.MESSAGE)

        contractor = self.contractor_service.create()

        return self.student_repository.create(student_in, contractor.id)

    def get_all(self) -> List[StudentSchemaOut]:
        students = self.student_repository.get_all()
        for student in students:
            responsibles_ = self.responsible_contract_service.get_contractor_id(
                student.contractor_id)
            resps = []
            for r in responsibles_:
                resps.append(r)
            student.responsibles = responsibles_

        return students

    def get_all_actives(self) -> List[StudentSchemaOut]:
        return self.student_repository.get_all_actives()

    def get_id(self, id: UUID) -> StudentSchemaOut:
        student = self.student_repository.get_id(id)
        if not student:
            raise ValueError(StudentNotFoundError.MESSAGE)

        student.responsibles = self.responsible_contract_service.get_contractor_id(
            student.contractor.id)
        student.plans = self.student_repository.student_health_plans(
            student.id)

        responsibles_ = self.responsible_contract_service.get_contractor_id(
            student.contractor_id)
        resps = []
        for r in responsibles_:
            resps.append(r)
        student.responsibles = responsibles_
        plans = []
        health_plans_ = self.student_repository.student_health_plans(
            student.id)
        for p in health_plans_:
            plans.append(p.plan)
        student.plans = plans

        return student

    def update_active(self, id: UUID) -> StudentSchemaOut:
        student = self.student_repository.get_id(id)
        if not student:
            raise ValueError(StudentNotFoundError.MESSAGE)

        if student.status == StatusEnum.ACTIVE:
            return self.student_repository.inactive(student)

        if student.status == StatusEnum.INACTIVE:
            return self.student_repository.active(student)

    def update(self, id: UUID, student_in: StudentSchemaIn) -> StudentSchemaOut:
        student = self.student_repository.get_id(id)
        if not student:
            raise ValueError(StudentNotFoundError.MESSAGE)

        return self.student_repository.update(student, student_in)

    def save_avatar(self, id: UUID, file: bytes) -> StudentSchemaOut:
        student = self.student_repository.get_id(id)
        if not student:
            raise ValueError(StudentNotFoundError.MESSAGE)

        path = 'public/avatars/students/' + str(student.id) + '.jpg'
        if student.avatar != None:
            os.remove(path)

        with open(path, 'wb') as f:
            f.write(file)

        return self.student_repository.save_avatar(student, path)

    def avatar(self, id: UUID):
        student = self.student_repository.get_id(id)
        if not student:
            raise ValueError(StudentNotFoundError.MESSAGE)

        return student.avatar

    def create_responsible(self, student_id: UUID, responsible_contract_in: ResponsibleContractSchemaIn) -> ResponsibleContractSchemaOut:
        student = self.student_repository.get_id(student_id)
        if not student:
            raise ValueError(StudentNotFoundError.MESSAGE)

        return self.responsible_contract_service.create(responsible_contract_in, student.contractor_id)

    def get_responsible_contractor(self, student_id: UUID) -> List[ResponsibleContractSchemaOut]:
        student = self.student_repository.get_id(student_id)
        if not student:
            raise ValueError(StudentNotFoundError.MESSAGE)

        return self.responsible_contract_service.get_contractor_id(student.contractor_id)

    def get_responsible_id(self, responsible_id: UUID) -> ResponsibleContractSchemaOut:
        return self.responsible_contract_service.get_id(responsible_id)

    def update_responsible(self, responsible_id: UUID, responsible_in: ResponsibleContractSchemaIn) -> ResponsibleContractSchemaOut:
        return self.responsible_contract_service.update(responsible_id, responsible_in)

    def remove_responsible(self, responsible_id: UUID) -> bool:
        return self.responsible_contract_service.remove(responsible_id)

    def create_address(self, student_id: UUID, address_in: AddressContractorSchemaIn) -> AddressContractorSchemaOut:
        student = self.student_repository.get_id(student_id)
        if not student:
            raise ValueError(StudentNotFoundError.MESSAGE)

        return self.address_contract_service.create(address_in, student.contractor_id)

    def get_address_contractor(self, student_id: UUID) -> AddressContractorSchemaOut:
        student = self.student_repository.get_id(student_id)
        if not student:
            raise ValueError(StudentNotFoundError.MESSAGE)
        return self.address_contract_service.get_contractor_id(student.contractor_id)

    def update_address(self, address_id: UUID, address_in: AddressContractorSchemaIn) -> AddressContractorSchemaOut:
        return self.address_contract_service.update(address_id, address_in)

    def filters(self, filters_in: Filters) -> List[StudentSchemaOut]:
        students = self.student_repository.get_filters(filters_in)
        for student in students:
            responsibles_ = self.responsible_contract_service.get_contractor_id(
                student.contractor_id)
            resps = []
            for r in responsibles_:
                resps.append(r)
            student.responsibles = responsibles_

        return students

    def create_student_health_plan(self, student_id: UUID, health_plan_id: UUID):
        plan = self.student_repository.student_health_plan_exists(
            student_id, health_plan_id)
        if plan:
            raise ValueError(PlanExistsError.MESSAGE)

        return self.student_repository.create_student_health_plan(student_id, health_plan_id)

    def remove_student_health_plan(self, student_id: UUID, health_plan_id: UUID) -> bool:
        return self.student_repository.remove_student_health_plan(student_id, health_plan_id)

    def student_health_plans(self, student_id: UUID) -> List[StudentPlanSchemaOut]:
        return self.student_repository.student_health_plans(student_id)

    def change_type_billing(self, contractor_id: UUID, contractor_in: ContractorIn) -> ContractorOut:
        return self.contractor_service.update(contractor_id, contractor_in)