from typing import Optional, List
from uuid import UUID
from pydantic import BaseModel
from schemas.execution_schemas import ExecutionOut
from schemas.student_schemas import StudentOut

class ProcedureIn(BaseModel):
    skill_id: Optional[UUID]
    name: str
    tries: int    
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
    schedule_id: Optional[UUID]
    skill_id: UUID
    procedure_id: Optional[UUID]
    skill_name: Optional[str]
    name: str
    tries: int    
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
    student: Optional[StudentOut]

    class Config:
        orm_mode = True

