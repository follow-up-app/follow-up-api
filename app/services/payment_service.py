import datetime
from typing import List
from uuid import UUID
from app.constants.exceptions.payment_exceptions import PaymentNotFoundError
from app.constants.exceptions.schedule_exceptions import ScheduleNotFoundError
from app.repositories.payment_repository import PaymnentRepository
from app.repositories.schedule_repository import ScheduleRepository
from app.schemas.payment_schemas import PaymentFilters, PaymentGroup, PaymentSchemaIn, PaymentSchemaOut
from app.schemas.schedule_schemas import ScheduleSchemaOut


class PaymentService:
    def __init__(self,
                 payment_repository: PaymnentRepository,
                 schedule_repository: ScheduleRepository):
        self.payment_repository = payment_repository
        self.schedule_repository = schedule_repository

    def create(self, schedule_id: UUID) -> PaymentSchemaOut:
        schedule = self.schedule_repository.get_id(schedule_id)
        if not schedule:
            raise ValueError(ScheduleNotFoundError.MESSAGE)

        value = schedule.specialty.value_hour
        date_due = datetime.date.today() + datetime.timedelta(days=30)

        return self.payment_repository.create(schedule.company_id, schedule.id, schedule.instructor_id, value, date_due)

    def get_id(self, id: UUID) -> PaymentSchemaOut:
        return self.payment_repository.get_id(id)

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
