from typing import Optional
from uuid import UUID
from pydantic import BaseModel, constr, Field

class ProcedureIn(BaseModel):
    program_id: UUID
    name: str
    objective: Optional[str]    
    stimulus: Optional[str]
    answer: Optional[str]
    consequence: Optional[str]
    material: Optional[str]
    type_help: Optional[str]
    attempts: Optional[str]
    goal_value: Optional[int]
    description: Optional[str]


class ProcedureOut(BaseModel):
    id: UUID
    program_id: UUID
    program_title: str
    name: str
    objective: Optional[str]    
    stimulus: Optional[str]
    answer: Optional[str]
    consequence: Optional[str]
    material: Optional[str]
    type_help: Optional[str]
    attempts: Optional[str]
    goal_value: Optional[int]
    description: Optional[str]

    class Config:
        orm_mode = True

