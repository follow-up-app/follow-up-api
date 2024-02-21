from datetime import datetime, date
from typing import Optional, List
from uuid import UUID
from pydantic import BaseModel
from db.models import StatusSchedule
from schemas.instructor_schema import InstructorOut
from schemas.student_schemas import StudentOut
from schemas.skill_schemas import SkillOut
from schemas.execution_schemas import ExecutionOut
from schemas.procedure_schemas import ProcedureOut


class SkillFollowUp(BaseModel):
    id: UUID
    schedule_id: UUID
    skill_id: UUID
    skill_name: str
    procedures: Optional[List[ProcedureOut]]

    class Config:
        orm_mode = True


class ScheduleFollowUp(BaseModel):
    id: UUID
    student_id: Optional[UUID]
    instructor_id: Optional[UUID]
    title: str
    start: datetime
    end: datetime
    details: Optional[str]
    student_arrival: Optional[datetime]
    event_begin: Optional[datetime]
    event_finish: Optional[datetime]
    event_user_id: Optional[UUID]
    status: Optional[StatusSchedule]
    student: Optional[StudentOut]
    instructor: Optional[InstructorOut]
    created_date: datetime
    updated_at: datetime
    skills: Optional[List[SkillFollowUp]]

    class Config:
        orm_mode = True


class ScheduleFollowUpMobile(BaseModel):
    id: UUID
    student_arrival: Optional[datetime]
    status: Optional[StatusSchedule]
    student: Optional[StudentOut]
    instructor: Optional[InstructorOut]
    skill: Optional[SkillOut]

    class Config:
        orm_mode = True


class Filters(BaseModel):
    student_id: Optional[UUID] = None
    start: Optional[date] = None
    end: Optional[date] = None
