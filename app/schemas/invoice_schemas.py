from typing import Optional, List
from uuid import UUID
from pydantic import BaseModel
from app.constants.enums.invoice_enum import InvoiceEnum


class InvoiceSchemaIn(BaseModel):
    id: UUID
    billings: List[UUID]
    student_id: Optional[UUID]
    responsible_id: Optional[UUID]
    health_plan_id: Optional[UUID]


class InvoiceSchemaOut(BaseModel):
    id: UUID
    company_id: UUID
    reference: str

    class Config:
        orm_mode = True


class InvoiceLogSchemaOut(BaseModel):
    id: UUID
    invoice_id: UUID
    history: str

    class Config:
        orm_mode = True


class InvoiceBillingSchemaOut(BaseModel):
    id: UUID
    invoice_id: UUID
    billing_id: UUID

    class Config:
        orm_mode = True
