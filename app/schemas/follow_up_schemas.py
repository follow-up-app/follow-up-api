from datetime import datetime, date
from typing import Optional, List
from uuid import UUID
from pydantic import BaseModel
from app.constants.enums.schedule_enum import ScheduleEnum
from app.schemas.instructor_schema import InstructorSchemaOut
from app.schemas.student_schemas import StudentSchemaOut
from app.schemas.skill_schemas import SkillSchemaOut
from app.schemas.procedure_schemas import ProcedureSchemaOut


class SkillFollowUp(BaseModel):
    id: UUID
    schedule_id: UUID
    skill_id: UUID
    skill_name: str
    procedures: List[ProcedureSchemaOut]

    class Config:
        orm_mode = True


class ScheduleSchemaFollowUp(BaseModel):
    id: UUID
    student_id: Optional[UUID]
    instructor_id: Optional[UUID]
    title: str
    start: datetime
    end: datetime
    start_hour: Optional[str]
    end_hour: Optional[str]
    details: Optional[str]
    student_arrival: Optional[datetime]
    event_begin: Optional[datetime]
    event_finish: Optional[datetime]
    event_user_id: Optional[UUID]
    status: Optional[ScheduleEnum]
    student: Optional[StudentSchemaOut]
    instructor: Optional[InstructorSchemaOut]
    created_date: datetime
    updated_at: datetime
    skills: Optional[List[SkillFollowUp]]

    class Config:
        orm_mode = True


class ScheduleSchemaFollowUpMobile(BaseModel):
    id: UUID
    student_arrival: Optional[datetime]
    status: Optional[ScheduleEnum]
    student: Optional[StudentSchemaOut]
    instructor: Optional[InstructorSchemaOut]
    skill: Optional[SkillSchemaOut]
    procedures: Optional[List[ProcedureSchemaOut]]
    outhers: Optional[List[ProcedureSchemaOut]]

    class Config:
        orm_mode = True


class FiltersSchemaIn(BaseModel):
    student_id: Optional[UUID] = None
    start: Optional[date] = None
    end: Optional[date] = None
