from datetime import datetime, timedelta
from typing import List
from uuid import UUID
from app.repositories.billing_repository import BillingRepository
from app.schemas.schedule_schemas import ScheduleSchemaOut
from app.schemas.student_schemas import StudentSchemaOut
from app.schemas.billing_schemas import BillingSchemaIn, BillingSchemaOut, BillingFilters, BillingGroup
from app.constants.enums.billing_enum import CategoryEnum, BillingEnum
from app.constants.exceptions.billing_exceptions import BillingNotFoundError


class BillingService:
    def __init__(self,
                 billing_repository: BillingRepository):
        self.billing_repository = billing_repository

    def create(self, schedule: ScheduleSchemaOut, student: StudentSchemaOut) -> BillingSchemaOut:
        value = schedule.specialty.value_hour
        category = CategoryEnum.PERSONAL
        if student.contractor.type_billing == CategoryEnum.PLAN:
            category = CategoryEnum.PLAN

        date_due_ = schedule.start + timedelta(days=30)
        date_due = date_due_.strftime("%Y-%m-%d")
        reference = date_due_.strftime("%m/%Y")

        return self.billing_repository.create(schedule.company_id, schedule.id, student.id, category, value, date_due, reference)

    def get_id(self, id: UUID) -> BillingSchemaOut:
        return self.billing_repository.get_id(id)

    def get_all(self) -> List[BillingSchemaOut]:
        return self.billing_repository.get_all()

    def update(self, id: UUID, billing_in: BillingSchemaIn) -> BillingSchemaOut:
        billing = self.billing_repository.get_id(id)
        if not billing:
            raise ValueError(BillingNotFoundError.MESSAGE)

        return self.billing_repository.update(billing, billing_in)

    def update_status_schedule(self, schedule_id: UUID) -> BillingSchemaOut:
        billing = self.billing_repository.get_schedule_id(schedule_id)
        if not billing:
            raise ValueError(BillingNotFoundError.MESSAGE)

        return self.billing_repository.update_status(billing, BillingEnum.SCHEDULED)

    def get_filters(self, filters_in: BillingFilters) -> List[BillingSchemaOut]:
        start = datetime.combine(filters_in.start, datetime.min.time())
        end = datetime.combine(filters_in.end, datetime.max.time())

        return self.billing_repository.get_filters(start, end, filters_in.student_id, filters_in.status)

    def get_resume(self, filters_in: BillingFilters) -> List[BillingGroup]:
        start = datetime.combine(filters_in.start, datetime.min.time())
        end = datetime.combine(filters_in.end, datetime.max.time())

        return self.billing_repository.get_resume(start, end, filters_in.status, filters_in.student_id)

    def get_student_status(self, filters_in: BillingFilters) -> List[BillingSchemaOut]:
        start = datetime.combine(filters_in.start, datetime.min.time())
        end = datetime.combine(filters_in.end, datetime.max.time())

        return self.billing_repository.get_student_status(start, end, filters_in.status, filters_in.student_id, filters_in.specialty_id)

    def delete_for_schedule(self, schedule_id: UUID) -> bool:
        return self.billing_repository.delete_for_schedule(schedule_id)

    def delete_invoice_billing(self, id: UUID) -> bool:
        return self.billing_repository.delete_invoice_billing(id)

    def update_many_status(self, ids: List[UUID], status: BillingEnum) -> bool:
        for id in ids:
            billing = self.billing_repository.get_id(id)
            if not billing:
                raise ValueError(BillingNotFoundError.MESSAGE)

            self.billing_repository.update_status(billing, status)

        return True

    def get_by_schedule_id(self, schedule_id: UUID) -> BillingSchemaOut:
        billing = self.billing_repository.get_schedule_id(schedule_id)
        if not billing:
            raise ValueError(BillingNotFoundError.MESSAGE)

        return billing