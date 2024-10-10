from uuid import UUID
from typing import Optional
from pydantic import BaseModel
from app.constants.enums.contract_enum import ContractEnum
from app.constants.enums.billing_enum import CategoryEnum


class ContractorIn(BaseModel):
    company_id: Optional[UUID]
    status: Optional[CategoryEnum]
    status: Optional[ContractEnum]


class ContractorOut(BaseModel):
    id: UUID
    company_id: UUID
    responsible_name: Optional[str]
    student_name: Optional[str]
    mode_billing: Optional[CategoryEnum] = None
    status: ContractEnum

    class Config:
        orm_mode = True
