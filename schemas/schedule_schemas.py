from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, constr, Field
from db.models import StatusSchedule

class ScheduleIn(BaseModel):
    student_id: Optional[UUID]
    instructor_id: Optional[UUID]
    skill_id:Optional[UUID]
    title: str
    start: datetime
    end: datetime
    details: Optional[str]
    status: Optional[StatusSchedule]

class ScheduleOut(BaseModel):
    id: UUID
    student_id: Optional[UUID]
    instructor_id: Optional[UUID]
    skill_id:Optional[UUID]
    title: str
    start: datetime
    end: datetime
    details: Optional[str]
    status: Optional[StatusSchedule]

    class Config:
        orm_mode = True