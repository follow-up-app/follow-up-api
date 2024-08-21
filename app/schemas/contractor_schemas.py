from uuid import UUID
from typing import Optional
from pydantic import BaseModel
from app.constants.enums.contract_enum import ContractEnum


class ContractorIn(BaseModel):
    company_id: Optional[UUID]
    status: Optional[ContractEnum]


class ContractorOut(BaseModel):
    id: UUID
    company_id: UUID
    responsible_name: Optional[str]
    student_name: Optional[str]
    status: ContractEnum

    class Config:
        orm_mode = True
