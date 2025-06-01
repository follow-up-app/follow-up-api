from typing import Optional, List
from uuid import UUID
from pydantic import BaseModel
from datetime import datetime
from app.constants.enums.invoice_enum import InvoiceSenderStatusEnum

class InvoiceSchemaIn(BaseModel):
    billings: List[UUID]
    student_id: UUID
    responsible_id: Optional[UUID] = None
    health_plan_id: Optional[UUID] = None


class InvoiceSchemaOut(BaseModel):
    id: UUID
    company_id: UUID
    reference: str
    api_status: Optional[str] = None
    sender_status: InvoiceSenderStatusEnum

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

    invoice: InvoiceSchemaOut

    class Config:
        orm_mode = True

class InvoiceSenderApi(BaseModel):
    cnpj_prestador: str
    ref: str
    status: str


class InvoiceResponseApi(BaseModel):
    cnpj_prestador: str
    ref: str
    numero_rps: str
    serie_rps: str
    status: str
    numero: str
    codigo_verificacao: str
    data_emissao: datetime
    url: str
    caminho_xml_nota_fiscal: str
    caminho_xml_cancelamento: Optional[str] = None

    class Config:
        orm_mode = True