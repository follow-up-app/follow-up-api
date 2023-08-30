from datetime import date
from typing import Optional, List
from uuid import UUID
from pydantic import BaseModel, constr, Field
from db.models import Status, Genere, BondPartenal


class AddressContractorIn(BaseModel):
    responsible_contract_id: Optional[UUID]
    address: str
    number: int
    complement: Optional[str]
    zip_code: str
    district: str
    city: str
    state: str


class AddressContractorOut(BaseModel):
    id: UUID
    responsible_contract_id: Optional[UUID]
    address: Optional[str]
    number: Optional[int]
    complement: Optional[str]
    zip_code: Optional[str]
    district: Optional[str]
    city: Optional[str]
    state: Optional[str]

    class Config:
        orm_mode = True


class ResponsibleContractIn(BaseModel):
    fullname: str
    birthday: date
    document: Optional[str]
    indentity_number: Optional[str]
    org_exp: Optional[str]
    uf_exp: Optional[str]
    nationality: Optional[str]
    email: Optional[str]
    phone: Optional[str]
    main_contract: Optional[str]
    bond:  Optional[str]


class ResponsibleContractOut(BaseModel):
    id: UUID
    contractor_id: UUID
    fullname: str
    birthday: date
    document: Optional[str]
    indentity_number: Optional[str]
    org_exp: Optional[str]
    uf_exp: Optional[str]
    nationality: Optional[str]
    email: Optional[str]
    phone: Optional[str]
    main_contract: Optional[str]
    bond:  Optional[str]

    class Config:
        orm_mode = True


class StudentIn(BaseModel):
    fullname: str
    birthday: date
    allergy: Optional[str]
    genere: Genere
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


class StudentOut(BaseModel):
    id: UUID
    contractor_id: UUID
    fullname: str
    birthday: date
    allergy: Optional[str]
    genere: Genere
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
    status: Status

    class Config:
        orm_mode = True


class ContractOut(BaseModel):
    id: UUID
    student: List[StudentOut]
    resposables: Optional[List[ResponsibleContractOut]]
    address: Optional[List[AddressContractorOut]]
    
    class Config:
        orm_mode = True
