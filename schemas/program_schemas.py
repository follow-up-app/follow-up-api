from uuid import UUID
from pydantic import BaseModel, constr, Field

class ProgramIn(BaseModel):
    title: str
    objective: str
    

class ProgramOut(BaseModel):
    id: UUID
    company_id: UUID
    title: str
    objective: str

    class Config:
        orm_mode = True