from datetime import datetime, date
from typing import Optional, List
from uuid import UUID
from pydantic import BaseModel, constr, Field
from db.models import StatusSchedule, EventRepeat
from schemas.instructor_schema import InstructorOut
from schemas.student_schemas import StudentOut
from schemas.skill_schemas import SkillOut

class ScheduleIn(BaseModel):
    student_id: Optional[UUID]
    instructor_id: Optional[UUID]
    skill_id: List[UUID]
    start_hour: str
    end_hour: str
    repeat: EventRepeat
    period: Optional[int]
    details: Optional[str]
    color: Optional[str]
    schedule_in: date
    
class ScheduleEvent(BaseModel):
    status: StatusSchedule


class SkillScehduleOut(BaseModel):
    id: UUID
    schedule_id: UUID
    skill_id: UUID
    skill_name: str
    
    class Config:
        orm_mode = True

class ScheduleOut(BaseModel):
    id: UUID
    student_id: Optional[UUID]
    instructor_id: Optional[UUID]
    event_id: Optional[UUID]
    title: str
    start: datetime
    end: datetime
    start_hour: Optional[str]
    end_hour: Optional[str]
    repeat: Optional[EventRepeat]
    period: Optional[str]
    color: Optional[str]
    details: Optional[str]
    event_begin: Optional[datetime]
    event_finish: Optional[datetime]
    event_user_id: Optional[UUID]
    status: Optional[StatusSchedule]
    student: Optional[StudentOut]
    instructor: Optional[InstructorOut]
    skills:  Optional[List[SkillScehduleOut]]
    created_date: datetime
    updated_at: datetime

    class Config:
        orm_mode = True



