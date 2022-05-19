from uuid import UUID
from pydantic import BaseModel, constr, Field

from db.models import MarkProcedure

class ProcedureIn(BaseModel):
    program_id: UUID
    mark: MarkProcedure
    level: int
    stimulus: str
    orientation_executation: str
    orientation_partial_executation: str
    points_total: int
    points_partial: int


class ProcedureOut(BaseModel):
    id: UUID
    program_id: UUID
    mark: MarkProcedure
    level: int
    stimulus: str
    orientation_executation: str
    orientation_partial_executation: str
    points_total: int
    points_partial: int

    class Config:
        orm_mode = True

