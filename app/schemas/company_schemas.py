from typing import Optional
from uuid import UUID
from pydantic import BaseModel
from app.constants.enums.company_enum import CompanyEnum


class CompanySchemaIn(BaseModel):
    name: str
    document: str
    municipal_registration: str
    address: str
    number_address: Optional[int]
    complement: Optional[str] = None
    zip_code: str
    city: str
    state: str
    country: str
    email: str
    phone: str
    city_code: Optional[str] = None
    aliquot: Optional[int] = None
    item_list_service: Optional[str] = None
    municipal_tax_code: Optional[str] = None
    api_nfes_token: Optional[str] = None


class CompanySchemaOut(BaseModel):
    id: UUID
    name: str
    document: str
    municipal_registration: str
    address: str
    number_address: Optional[int]
    complement: Optional[str] = None
    zip_code: str
    city: str
    state: str
    country: str
    email: str
    phone: str
    city_code: Optional[str] = None
    aliquot: Optional[int] = None
    item_list_service: Optional[str] = None
    municipal_tax_code: Optional[str] = None
    api_nfes_token: Optional[str] = None

    class Config:
        orm_mode = True


class CompanyInvoiceTokenSchemaOut(BaseModel):
    id: UUID
    token: str

    class Config:
        orm_mode = True
