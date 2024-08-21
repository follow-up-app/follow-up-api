from typing import Optional
from uuid import UUID
from pydantic import BaseModel
from app.constants.enums.company_enum import CompanyEnum


class CompanySchemaIn(BaseModel):
    name: str
    document: str
    address: str
    number_address: Optional[int]
    complement: Optional[str]
    zip_code: str
    city: str
    state: str
    country: str
    email: str
    phone: str
    status: Optional[CompanyEnum]


class CompanySchemaOut(BaseModel):
    id: UUID
    name: str
    document: str
    address: str
    number_address: Optional[int]
    complement: Optional[str]
    zip_code: str
    city: str
    state: str
    country: str
    email: str
    phone: str
    status: CompanyEnum

    class Config:
        orm_mode = True
