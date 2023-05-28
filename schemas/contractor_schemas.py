from uuid import UUID
from typing import Optional
from pydantic import BaseModel
from db.models import StatusContract


class ContractorIn(BaseModel):
    company_id: UUID
    fullname: str
    document: str
    indentity_number: Optional[str]
    email: str


class ContractorOut(BaseModel):
    id: UUID
    company_id: UUID
    responsible_name: Optional[str]
    student_name: Optional[str]
    status: StatusContract

    class Config:
        orm_mode = True


class ResponsibleContractIn(BaseModel):
    contractor_id: UUID
    user_id: Optional[UUID]
    fullname: str
    document: str
    indentity_number: Optional[str]
    email: str


class ResponsibleContractOut(BaseModel):
    id: UUID
    contractor_id: UUID
    user_id: Optional[UUID]
    fullname: str
    document: str
    indentity_number: Optional[str]
    email: str

    class Config:
        orm_mode = True



class AddressContractIn(BaseModel):
    responsible_contract_id: UUID
    address: str
    complement: Optional[str]
    zip_code: str
    district: Optional[str]
    city: str
    state: str

class AddressContractOut(BaseModel):
    id: UUID
    responsible_contract_id: UUID
    address: str
    complement: Optional[str]
    zip_code: str
    district: Optional[str]
    city: str
    state: str

    class Config:
        orm_mode = True
