from uuid import UUID
from typing import Optional
from datetime import datetime

from pydantic import BaseModel


class InstructorIn(BaseModel):
    specialty: Optional[UUID]
    fullname: str
    document: str
    email: str
    phone: Optional[str]
    indentity_number: Optional[UUID]
    org_exp: Optional[UUID]
    uf_exp: Optional[UUID]
    nationality: Optional[UUID]
    birthday: datetime
    document_company: Optional[str]
    social_name: Optional[str]
    fantasy_name: Optional[str]
    value_hour: Optional[str]
    value_mouth: Optional[str]
    comission: Optional[str]


class InstructorOut(BaseModel):
    id: UUID
    company_id: UUID
    user_id: Optional[UUID]
    specialty_instructor_id: Optional[UUID]
    fullname: str
    document: str
    email: str
    phone: Optional[str]
    indentity_number: Optional[UUID]
    org_exp: Optional[UUID]
    uf_exp: Optional[UUID]
    nationality: Optional[UUID]
    birthday: datetime
    document_company: Optional[str]
    social_name: Optional[str]
    fantasy_name: Optional[str]
    value_hour: Optional[str]
    value_mouth: Optional[str]
    comission: Optional[str]
    status: Optional[bool]    

    class Config:
        orm_mode = True