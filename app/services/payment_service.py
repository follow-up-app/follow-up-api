import datetime
from typing import List
from uuid import UUID
from app.constants.enums.instructor_payments_enum import ModePaymentEnum
from app.constants.enums.payment_enum import PaymentEnum
from app.constants.exceptions.payment_exceptions import PaymentNotFoundError
from app.constants.exceptions.schedule_exceptions import ScheduleNotFoundError
from app.repositories.payment_repository import PaymnentRepository
from app.repositories.schedule_repository import ScheduleRepository
from app.schemas.instructor_schema import InstructorSchemaOut
from app.schemas.payment_schemas import PaymentFilters, PaymentGroup, PaymentSchemaIn, PaymentSchemaOut
from app.schemas.schedule_schemas import ScheduleSchemaOut


class PaymentService:
    def __init__(self,
                 payment_repository: PaymnentRepository):
        self.payment_repository = payment_repository

    def create(self, schedule: ScheduleSchemaOut, instructor: InstructorSchemaOut) -> PaymentSchemaOut:
        value = None
        if instructor.mode_payment == ModePaymentEnum.HOUR:
            value = instructor.value

        date_due = datetime.date.today() + datetime.timedelta(days=30)

        return self.payment_repository.create(schedule.company_id, schedule.id, instructor.id, value, date_due)

    def get_id(self, id: UUID) -> PaymentSchemaOut:
        return self.payment_repository.get_id(id)

    def update_status_schedule(self, schedule_id: UUID) -> PaymentSchemaOut:
        payment = self.payment_repository.get_schedule_id(schedule_id)
        if not payment:
            raise ValueError(PaymentNotFoundError.MESSAGE)

        return self.payment_repository.update_status(payment, PaymentEnum.SCHEDULED)

    def get_all(self) -> List[PaymentSchemaOut]:
        return self.payment_repository.get_all()

    def update(self, id: UUID, payment_in: PaymentSchemaIn) -> PaymentSchemaOut:
        payment = self.payment_repository.get_id(id)
        if not payment:
            raise ValueError(PaymentNotFoundError.MESSAGE)

        return self.payment_repository.update(payment, payment_in)

    def get_filters(self, filters_in: PaymentFilters) -> List[PaymentSchemaOut]:
        start = datetime.combine(filters_in.start, datetime.min.time())
        end = datetime.combine(filters_in.end, datetime.max.time())

        return self.payment_repository.get_filters(start, end, filters_in.instructor_id, filters_in.status)

    def get_resume(self, filters_in: PaymentFilters) -> List[PaymentGroup]:
        start = datetime.combine(filters_in.start, datetime.min.time())
        end = datetime.combine(filters_in.end, datetime.max.time())

        return self.payment_repository.get_resume(start, end, filters_in.status)
