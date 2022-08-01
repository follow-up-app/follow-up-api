from uuid import UUID
from pydantic import BaseModel, constr, Field

class ProgramIn(BaseModel):
    title: str
    description: str
    

class ProgramOut(BaseModel):
    id: UUID
    company_id: UUID
    title: str
    description: str

    class Config:
        orm_mode = True