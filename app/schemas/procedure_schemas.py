from typing import Optional, List
from uuid import UUID
from pydantic import BaseModel
from app.schemas.execution_schemas import ExecutionSchemaOut
from app.schemas.student_schemas import StudentSchemaOut

class ProcedureSchemaIn(BaseModel):
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


class ProcedureSchemaOut(BaseModel):
    id: UUID
    schedule_id: Optional[UUID]
    skill_id: UUID
    student_id: Optional[UUID]
    procedure_id: Optional[UUID]
    skill_name: Optional[str]
    name: str
    tries: int    
    goal: float
    period: str
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
    executions: Optional[List[ExecutionSchemaOut]]
    student: Optional[StudentSchemaOut]

    class Config:
        orm_mode = True

