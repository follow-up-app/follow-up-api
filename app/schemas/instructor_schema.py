from uuid import UUID
from typing import Optional
from datetime import date
from pydantic import BaseModel
from app.constants.enums.status_enum import StatusEnum


class InstructorSchemaIn(BaseModel):
    fullname: str
    document: Optional[str]
    email: Optional[str]
    phone: Optional[str]
    indentity_number: Optional[str]
    org_exp: Optional[str]
    uf_exp: Optional[str]
    nationality: Optional[str]
    birthday: date
    document_company: Optional[str]
    social_name: Optional[str]
    fantasy_name: Optional[str]
    comission: Optional[str]
    status: Optional[StatusEnum]


class InstructorSchemaOut(BaseModel):
    id: UUID
    company_id: UUID
    user_id: Optional[UUID]
    fullname: str
    document: str
    email: str
    phone: Optional[str]
    indentity_number: Optional[str]
    org_exp: Optional[str]
    uf_exp: Optional[str]
    nationality: Optional[str]
    birthday: date
    document_company: Optional[str]
    social_name: Optional[str]
    fantasy_name: Optional[str]
    avatar: Optional[str]
    status: StatusEnum

    class Config:
        orm_mode = True


class Filters(BaseModel):
    instructor_id: Optional[UUID] = None
