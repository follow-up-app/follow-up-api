from uuid import UUID
from pydantic import BaseModel, constr, Field

class ProgramIn(BaseModel):
    title: str
    objetive: str
    

class ProgramOut(BaseModel):
    company_id: UUID
    title: str
    objetive: str

    class Config:
        orm_mode = True