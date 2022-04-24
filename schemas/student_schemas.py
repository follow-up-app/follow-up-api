from uuid import UUID
from pydantic import BaseModel, constr, Field

class StudentIn(BaseModel):
    fullname: str
    age: str
    

class StudentOut(BaseModel):
    company_id: UUID
    parent: UUID
    fullname: str
    age: str

    class Config:
        orm_mode = True