from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, constr, Field
from db.models import StatusSchedule
from schemas.instructor_schema import InstructorOut
from schemas.student_schemas import StudentOut
from schemas.skill_schemas import SkillOut

class ScheduleIn(BaseModel):
    student_id: Optional[UUID]
    instructor_id: Optional[UUID]
    skill_id:Optional[UUID]
    title: str
    details: Optional[str]
    color: Optional[str]
    status: Optional[StatusSchedule]
    schedule_in: datetime
    schedule_out: datetime
    
class ScheduleEvent(BaseModel):
    status: StatusSchedule


class ScheduleOut(BaseModel):
    id: UUID
    student_id: Optional[UUID]
    instructor_id: Optional[UUID]
    skill_id:Optional[UUID]
    title: str
    start: datetime
    end: datetime
    color: Optional[str]
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

    class Config:
        orm_mode = True

