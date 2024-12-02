from datetime import date
from typing import Optional, List
from uuid import UUID
from pydantic import BaseModel
from app.constants.enums.genere_enum import GenereEnum
from app.constants.enums.status_enum import StatusEnum
from app.schemas.responsible_contract_schemas import ResponsibleContractSchemaOut
from app.schemas.contractor_schemas import ContractorOut
from app.schemas.health_plan_schemas import HealthPlanSchemaOut


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
    plans: Optional[List[HealthPlanSchemaOut]]
    contractor: Optional[ContractorOut]
    status: StatusEnum

    class Config:
        orm_mode = True


class StudentPlanSchemaIn(BaseModel):
    student_id: UUID
    health_plan_id: UUID


class StudentPlanSchemaOut(BaseModel):
    student_id: UUID
    health_plan_id: UUID
    plan: HealthPlanSchemaOut

    class Config:
        orm_mode = True


class Filters(BaseModel):
    student_id: Optional[UUID] = None
