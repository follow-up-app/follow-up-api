from datetime import date
from typing import Optional, List
from uuid import UUID
from pydantic import BaseModel
from app.constants.enums.billing_enum import BillingEnum
from app.schemas.schedule_schemas import ScheduleSchemaOut
from app.schemas.student_schemas import StudentSchemaOut


class BillingSchemaIn(BaseModel):
    company_id: Optional[UUID]
    schedule_id: Optional[UUID]
    student_id: Optional[UUID]
    value: Optional[float] = None
    date_due: Optional[date] = None
    date_done: Optional[date] = None
    status: Optional[BillingEnum] = None


class BillingSchemaOut(BaseModel):
    id: UUID
    schedule_id: UUID
    student_id: UUID
    value: Optional[float] = None
    reference: Optional[str] = None
    date_due: Optional[date]
    date_done: Optional[date]
    schedule: Optional[ScheduleSchemaOut]
    student: Optional[StudentSchemaOut]
    status: BillingEnum

    class Config:
        orm_mode = True


class BillingFilters(BaseModel):
    student_id: Optional[UUID] = None
    specialty_id: Optional[UUID] = None
    start: Optional[date] = None
    end: Optional[date] = None
    status: Optional[BillingEnum] = None


class ManyBillingUpdate(BaseModel):
    ids: List[UUID]
    status: BillingEnum


class BillingGroup(BaseModel):
    schedule_id: UUID
    student_id: UUID
    count: int
    total: float
    status: BillingEnum
    schedule: ScheduleSchemaOut
    student: StudentSchemaOut

    class Config:
        orm_mode = True
