from typing import Optional, List
from uuid import UUID
from pydantic import BaseModel
from app.schemas.procedure_schemas import ProcedureSchemaOut
from app.schemas.specialty_schemas import SpecialtySchemaOut


class SkillSchemaIn(BaseModel):
    specialty_id: UUID
    name: str
    objective: str


class SkillSchemaOut(BaseModel):
    id: UUID
    specialty_id: Optional[UUID] = None
    name: str
    objective: str
    specialty_name: Optional[str]
    specialty: Optional[SpecialtySchemaOut]
    procedures: Optional[List[ProcedureSchemaOut]]

    class Config:
        orm_mode = True


class SkillManyIDs(BaseModel):
    skills: List[UUID]
