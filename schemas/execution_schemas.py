from datetime import datetime
from typing import Optional, List
from uuid import UUID
from pydantic import BaseModel
from db.models import TypeHelp

class ExecutionIn(BaseModel):
    schedule_id: UUID
    procedure_id: UUID
    trie: int
    time: str
    help_type: TypeHelp

class ExecutionOut(BaseModel):
    id: UUID
    schedule_id: UUID
    procedure_id: UUID
    procedure_schedule_id: Optional[UUID]
    trie: int
    time: str
    help_type: Optional[TypeHelp]
    success: bool
    user_id: UUID
    created_date: datetime

    class Config:
        orm_mode = True
