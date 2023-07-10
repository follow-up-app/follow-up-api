from typing import Optional
from uuid import UUID
from pydantic import BaseModel

class ProcedureIn(BaseModel):
    skill_id: UUID
    name: str
    tries: int    
    time: str
    goal: float
    period: str
    name: str
    objective: Optional[str]    
    stimulus: Optional[str]
    answer: Optional[str]
    consequence: Optional[str]
    materials: Optional[str]
    help: Optional[str]


class ProcedureOut(BaseModel):
    id: UUID
    skill_id: UUID
    skill_name = str
    name: str
    tries: int    
    time: str
    goal: float
    period: str
    name: str
    objective: Optional[str]    
    stimulus: Optional[str]
    answer: Optional[str]
    consequence: Optional[str]
    materials: Optional[str]
    help: Optional[str]

    class Config:
        orm_mode = True

