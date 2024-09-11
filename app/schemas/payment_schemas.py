from datetime import date
from typing import Optional
from uuid import UUID
from pydantic import BaseModel
from app.constants.enums.payment_enum import PaymentEnum
from app.schemas.instructor_schema import InstructorSchemaOut
from app.schemas.schedule_schemas import ScheduleSchemaOut


class PaymentSchemaIn(BaseModel):
    company_id: Optional[UUID]
    schedule_id: UUID
    instructor_id: UUID
    value: Optional[float] = None
    date_due: Optional[date] = None
    date_scheduled: Optional[date] = None
    date_done: Optional[date] = None
    status: Optional[PaymentEnum] = None


class PaymentSchemaOut(BaseModel):
    id: UUID
    schedule_id: UUID
    instructor_id: UUID
    value: float
    date_due: Optional[date]
    date_scheduled: Optional[date]
    date_done: Optional[date]
    schedule: Optional[ScheduleSchemaOut]
    instructor: Optional[InstructorSchemaOut]
    status: PaymentEnum

    class Config:
        orm_mode = True


class PaymentFilters(BaseModel):
    instructor_id: Optional[UUID] = None
    start: Optional[date] = None
    end: Optional[date] = None
    status: Optional[PaymentEnum] = None


class PaymentGroup(BaseModel):
    schedule_id: UUID
    instructor_id: UUID
    count: int
    total: float
    schedule: ScheduleSchemaOut
    instructor: InstructorSchemaOut

    class Config:
        orm_mode = True
