from datetime import datetime
from uuid import UUID
from pydantic import BaseModel
from app.constants.enums.help_enum import HelpEnum


class ExecutionSchemaIn(BaseModel):
    schedule_id: UUID
    procedure_id: UUID
    trie: int
    time: str
    help_type: HelpEnum


class ExecutionSchemaOut(BaseModel):
    id: UUID
    schedule_id: UUID
    procedure_id: UUID
    procedure_schedule_id: UUID
    trie: int
    time: str
    help_type: HelpEnum
    success: bool
    user_id: UUID
    created_date: datetime

    class Config:
        orm_mode = True
