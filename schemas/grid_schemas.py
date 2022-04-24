from uuid import UUID
from pydantic import BaseModel, constr, Field

from db.models import StatusGrid


class GridIn(BaseModel):
    program_id: UUID
    student_id: UUID
    aplicator: UUID
    status: StatusGrid = None


class GridOut(BaseModel):
    program_id: UUID
    student_id: UUID
    aplicator: UUID
    status: StatusGrid

    class Config:
        orm_mode = True
