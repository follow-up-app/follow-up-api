from datetime import date
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, constr, Field

class StudentIn(BaseModel):
    fullname: str
    birthday: Optional[date]
    instructor: Optional[UUID]
    age: Optional[str]
    

class StudentOut(BaseModel):
    id: UUID
    company_id: UUID
    instructor: Optional[UUID]
    parent: Optional[UUID]
    fullname: str
    birthday: Optional[date]
    age: Optional[str]

    class Config:
        orm_mode = True