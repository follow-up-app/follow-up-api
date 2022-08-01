from uuid import UUID
from pydantic import BaseModel, constr, Field

class ResultIn(BaseModel):
    procedure_id: UUID
    student_id: UUID
    points_made: str
    anotations: str


class ResultOut(BaseModel):
    procedure_id: UUID
    student_id: UUID
    points_made: str
    anotations: str

    class Config:
        orm_mode = True