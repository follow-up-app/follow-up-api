from datetime import datetime, date
from typing import Optional, List
from uuid import UUID
from pydantic import BaseModel
from app.constants.enums.repeat_enum import RepeatEnum
from app.constants.enums.schedule_enum import ScheduleEnum
from app.schemas.instructor_schema import InstructorSchemaOut
from app.schemas.procedure_schemas import ProcedureSchemaOut
from app.schemas.specialty_schemas import SpecialtySchemaOut
from app.schemas.student_schemas import StudentSchemaOut


class SlotHourIn(BaseModel):
    start_hour: str
    end_hour: str


class ScheduleSchemaIn(BaseModel):
    id: Optional[UUID]
    student_id: UUID
    instructor_id: UUID
    specialty_id: UUID
    start_hour: str
    end_hour: str
    repeat: RepeatEnum
    period: Optional[int] = None
    details: Optional[str]
    color: Optional[str]
    schedule_in: date
    time_slots: List[SlotHourIn]
    procedures: List[ProcedureSchemaOut]
    dates: Optional[List[date]] = None


class ScheduleSchemaEvent(BaseModel):
    student_id: UUID
    instructor_id: UUID
    event_id: UUID
    specialty_id: Optional[UUID] = None
    title: str
    start: datetime
    end: datetime
    start_hour: Optional[str]
    end_hour: Optional[str]
    repeat: Optional[RepeatEnum]
    period: Optional[int] = None
    color: Optional[str]
    status: Optional[ScheduleEnum]


class ScheduleUpadateSchamaIn(BaseModel):
    status: ScheduleEnum


class ProcedureScheduleSchemaIn(BaseModel):
    procedure_id: UUID


class SkillScheduleSchemaOut(BaseModel):
    id: UUID
    schedule_id: UUID
    skill_id: UUID
    skill_name: str
    finished: bool
    event_id: UUID

    class Config:
        orm_mode = True


class ScheduleSchemaOut(BaseModel):
    id: UUID
    company_id: Optional[UUID]
    student_id: Optional[UUID]
    instructor_id: Optional[UUID]
    event_id: Optional[UUID]
    specialty_id: Optional[UUID] = None
    title: str
    start: datetime
    end: datetime
    start_hour: Optional[str]
    end_hour: Optional[str]
    repeat: Optional[RepeatEnum]
    period: Optional[str] = None
    color: Optional[str]
    details: Optional[str]
    event_begin: Optional[datetime]
    event_finish: Optional[datetime]
    event_user_id: Optional[UUID]
    student_arrival: Optional[datetime]
    status: Optional[ScheduleEnum]
    student: Optional[StudentSchemaOut]
    instructor: Optional[InstructorSchemaOut]
    skills: Optional[List[SkillScheduleSchemaOut]]
    procedures: Optional[List[ProcedureSchemaOut]]
    specialty: Optional[SpecialtySchemaOut]
    created_date: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class SkillScheduleIn(BaseModel):
    skill_id: UUID
