from typing import Optional
from uuid import UUID
from pydantic import BaseModel
from app.constants.enums.instructor_payments_enum import ModePaymentEnum, TypePaymentEnum


class InstructorPaymentSchemaIn(BaseModel):
    specialty_id: UUID
    type_payment: TypePaymentEnum
    mode_payment: ModePaymentEnum
    comission: Optional[float] = None
    value: float
    key: Optional[str] = None
    bank_number: Optional[int] = None
    account_number: Optional[str] = None


class InstructorPaymentSchemaOut(BaseModel):
    id: UUID
    bank_number: Optional[int] = None
    account_number: Optional[str] = None
    key: Optional[str] = None

    class Config:
        orm_mode = True