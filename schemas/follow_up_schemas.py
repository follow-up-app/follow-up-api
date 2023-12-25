from datetime import datetime, date
from typing import Optional, List
from uuid import UUID
from pydantic import BaseModel, constr, Field
from db.models import StatusSchedule
from schemas.instructor_schema import InstructorOut
from schemas.student_schemas import StudentOut
from schemas.skill_schemas import SkillOut
from schemas.execution_schemas import ExecutionOut

class FollowUpResult(BaseModel):
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
    points: float
    executions: List[ExecutionOut]
    
    class Config:
        orm_mode = True
    

class ScheduleFollowUp(BaseModel):
    id: UUID
    student_id: Optional[UUID]
    instructor_id: Optional[UUID]
    skill_id:Optional[UUID]
    title: str
    start: datetime
    end: datetime
    details: Optional[str]
    event_begin: Optional[datetime]
    event_finish: Optional[datetime]
    event_user_id: Optional[UUID]
    status: Optional[StatusSchedule]
    student: Optional[StudentOut]
    instructor: Optional[InstructorOut]
    skill: Optional[SkillOut]
    created_date: datetime
    updated_at: datetime
    results: Optional[List[FollowUpResult]]

    class Config:
        orm_mode = True
    

class Filters(BaseModel):
    student_id: Optional[UUID] = None
    start: Optional[date] = None
    end: Optional[date] = None
    