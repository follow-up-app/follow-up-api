from typing import Optional
from uuid import UUID
from pydantic import BaseModel
from app.constants.enums.company_enum import CompanyEnum


class CompanySchemaIn(BaseModel):
    social_name: str
    fantasy_name: Optional[str] = None
    document: str
    municipal_registration: Optional[str] = None
    address: str
    number_address: Optional[int]
    complement: Optional[str] = None
    zip_code: str
    district: str
    city: str
    state: str
    email: str
    phone: str
    city_code: Optional[str] = None
    aliquot: Optional[int] = None
    iss_retained: Optional[bool] = None
    licences_n: Optional[int] = None
    api_nfes_token: Optional[str] = None
    status: Optional[CompanyEnum]


class CompanySchemaOut(BaseModel):
    id: UUID
    fantasy_name: str
    social_name: str
    document: str
    address: str
    number_address:int
    complement: Optional[str] = None
    zip_code: str
    district: str
    city: str
    state: str
    email: str
    phone: str
    city_code: str
    aliquot: Optional[int] = None
    iss_retained: Optional[bool] = None
    licences_n: int
    api_nfes_token: Optional[str] = None
    status: CompanyEnum

    class Config:
        orm_mode = True


class CompanyInvoiceTokenSchemaOut(BaseModel):
    id: UUID
    token: str

    class Config:
        orm_mode = True
