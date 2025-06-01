from datetime import date
from typing import Optional
from uuid import UUID
from pydantic import BaseModel
from app.constants.enums.payment_enum import OrderPaymentEnum

class OrderPaymentSchemaOut(BaseModel):
    company_id: Optional[UUID]
    instructor_id: UUID
    period_reference: str
    number: str
    description: Optional[str] = None
    value: float
    date_due: date
    date_done: Optional[date] = None
    status: OrderPaymentEnum

    class Config:
        orm_mode = True


class OrderPaymentSchemaIn(BaseModel):
    period_reference: str
    description: Optional[str] = None
    value: float
    date_due: date
    date_done: Optional[date] = None
