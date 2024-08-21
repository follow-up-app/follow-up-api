from datetime import date
from typing import Optional
from uuid import UUID
from pydantic import BaseModel

from app.constants.enums.partenal_enum import PartenalEnum


class ResponsibleContractSchemaIn(BaseModel):
    fullname: str
    birthday: Optional[date]
    document: Optional[str]
    indentity_number: Optional[str]
    org_exp: Optional[str]
    uf_exp: Optional[str]
    nationality: Optional[str]
    email: Optional[str]
    phone: Optional[str]
    main_contract: Optional[str]
    bond:  Optional[PartenalEnum]


class ResponsibleContractSchemaOut(BaseModel):
    id: UUID
    contractor_id: UUID
    fullname: str
    birthday: Optional[date]
    document: Optional[str]
    indentity_number: Optional[str]
    org_exp: Optional[str]
    uf_exp: Optional[str]
    nationality: Optional[str]
    email: Optional[str]
    phone: Optional[str]
    main_contract: Optional[str]
    bond:  Optional[PartenalEnum]

    class Config:
        orm_mode = True