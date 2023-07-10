from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, constr, Field

from db.models import StatusGrid


class GridIn(BaseModel):
    skill_id: UUID
    student_id: UUID
    date_schedule: Optional[datetime]
    time_preview: Optional[str]
    observation: Optional[str]
    date_start: Optional[datetime]
    date_finish: Optional[datetime]
    status: Optional[StatusGrid]


class GridOut(BaseModel):
    id: UUID
    program_id: UUID
    student_id: UUID
    date_schedule: Optional[datetime]
    time_preview: Optional[str]
    observation: Optional[str]
    time_preview: Optional[str]
    observation: Optional[str]
    date_start: Optional[datetime]
    date_finish: Optional[datetime]
    status: Optional[StatusGrid]
    skill_name: str
    instructor_name: str
    student_name: str
    status: Optional[StatusGrid]

    class Config:
        orm_mode = True
