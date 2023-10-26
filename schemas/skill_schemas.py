from datetime import date
from typing import Optional, List
from uuid import UUID
from pydantic import BaseModel
from db.models import Status
from schemas.procedure_schemas import ProcedureOut


class SkillIn(BaseModel):
    name: str
    objective: str


class SkillOut(BaseModel):
    id: UUID
    name: str
    objective: str
    procedures: Optional[List[ProcedureOut]]

    class Config:
        orm_mode = True