from uuid import UUID
from typing import Optional
from datetime import datetime, date
from db.models import Status
from pydantic import BaseModel
from typing import List

class AddressInstructorIn(BaseModel):
    address: str
    number: int
    complement: Optional[str]
    zip_code: str
    district: str
    city: str
    state: str

class AddressInstructorOut(BaseModel):
    id: UUID
    address: Optional[str]
    number: Optional[int]
    complement: Optional[str]
    zip_code: Optional[str]
    district: Optional[str]
    city: Optional[str]
    state: Optional[str]

    class Config:
        orm_mode = True

class InstructorIn(BaseModel):
    # specialty: Optional[UUID]
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
    value_hour: Optional[str]
    value_mouth: Optional[str]
    comission: Optional[str]
    status: Optional[Status]
   
    

class InstructorOut(BaseModel):
    id: UUID
    company_id: UUID
    user_id: Optional[UUID]
    # specialty_instructor_id: Optional[UUID]
    specialty_name: Optional[str]
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
    value_hour: Optional[str]
    value_mouth: Optional[str]
    comission: Optional[str]
    avatar: Optional[str]
    status: Status
    
    class Config:
        orm_mode = True
        
class Filters(BaseModel):
    instructor_id: Optional[UUID] = None

