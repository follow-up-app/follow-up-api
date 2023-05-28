from uuid import UUID
from pydantic import BaseModel, constr, Field
from typing import Optional
from datetime import datetime


class ResultIn(BaseModel):
    procedure_id: UUID
    student_id: UUID
    instructor_id: UUID
    attempts: Optional [int]
    anotations: Optional [str]
    date_start: Optional [datetime]
    date_finish: Optional[datetime]


class ResultOut(BaseModel):
    id: UUID
    procedure_id: UUID
    student_id: UUID
    instructor_id: UUID
    attempts: Optional [int]
    points_made: Optional [str]
    anotations: Optional [str]
    date_start: Optional [datetime]
    date_finish: Optional[datetime]


    class Config:
        orm_mode = True