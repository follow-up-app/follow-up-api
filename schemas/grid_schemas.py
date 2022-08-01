from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, constr, Field

from db.models import StatusGrid


class GridIn(BaseModel):
    program_id: UUID
    student_id: UUID
    status: Optional[StatusGrid]


class GridOut(BaseModel):
    id: UUID
    program_id: UUID
    student_id: UUID
    aplicator: UUID
    program_title: str
    student_name: str
    status: Optional[StatusGrid]
    created_date: datetime

    class Config:
        orm_mode = True
