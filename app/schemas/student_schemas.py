from datetime import date
from typing import Optional, List
from uuid import UUID
from pydantic import BaseModel
from app.constants.enums.genere_enum import GenereEnum
from app.constants.enums.partenal_enum import PartenalEnum
from app.constants.enums.status_enum import StatusEnum
from app.schemas.responsible_contract_schemas import ResponsibleContractSchemaOut


class StudentSchemaIn(BaseModel):
    fullname: str
    birthday: date
    allergy: Optional[str]
    genere: GenereEnum
    document: Optional[str]
    indentity_number: Optional[str]
    org_exp: Optional[str]
    uf_exp: Optional[str]
    nationality: Optional[str]
    email: Optional[str]
    uf_exp: Optional[str]
    phone: Optional[str]
    informations: Optional[str]
    avatar: Optional[str]


class StudentSchemaOut(BaseModel):
    id: UUID
    contractor_id: UUID
    fullname: str
    birthday: date
    allergy: Optional[str]
    genere: GenereEnum
    document: Optional[str]
    indentity_number: Optional[str]
    org_exp: Optional[str]
    uf_exp: Optional[str]
    nationality: Optional[str]
    email: Optional[str]
    uf_exp: Optional[str]
    phone: Optional[str]
    informations: Optional[str]
    avatar: Optional[str]
    responsibles: Optional[List[ResponsibleContractSchemaOut]]
    status: StatusEnum

    class Config:
        orm_mode = True


class Filters(BaseModel):
    student_id: Optional[UUID] = None
