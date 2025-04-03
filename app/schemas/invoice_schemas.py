from typing import Optional, List
from uuid import UUID
from pydantic import BaseModel
from datetime import datetime

class InvoiceSchemaIn(BaseModel):
    billings: List[UUID]
    student_id: UUID
    # responsible_id: Optional[UUID] = None
    health_plan_id: Optional[UUID] = None


class InvoiceSchemaOut(BaseModel):
    id: UUID
    company_id: UUID
    reference: str
    api_status: str

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
    url_danfse: str