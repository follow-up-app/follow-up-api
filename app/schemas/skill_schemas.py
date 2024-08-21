from typing import Optional, List
from uuid import UUID
from pydantic import BaseModel
from app.schemas.procedure_schemas import ProcedureSchemaOut


class SkillSchemaIn(BaseModel):
    name: str
    objective: str


class SkillSchemaOut(BaseModel):
    id: UUID
    name: str
    objective: str
    procedures: Optional[List[ProcedureSchemaOut]]

    class Config:
        orm_mode = True
        
        
class SkillManyIDs(BaseModel):
    skills: List[UUID]