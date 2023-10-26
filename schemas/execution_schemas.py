from datetime import datetime
from typing import Optional, List
from uuid import UUID
from pydantic import BaseModel
from schemas.procedure_schemas import ProcedureOut
from db.models import HelpTypeExecution

class ExecutionIn(BaseModel):
    schedule_id: UUID
    procedure_id: UUID
    trie: int
    time: str
    help_type: HelpTypeExecution
    success: bool


class ExecutionOut(BaseModel):
    id: UUID
    schedule_id: UUID
    procedure_id: UUID
    trie: int
    time: str
    # help_type: Optional[HelpTypeExecution]
    success: bool
    user_id: UUID
    created_date: datetime
    # procedure: ProcedureOut

    class Config:
        orm_mode = True
