from typing import Optional, List
from uuid import UUID
from pydantic import BaseModel
from schemas.execution_schemas import ExecutionOut

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
    points: Optional[float]
    total_exec: Optional[int]
    data_chart: Optional[float]
    app_active: Optional[bool]
    executions: Optional[List[ExecutionOut]]

    class Config:
        orm_mode = True

