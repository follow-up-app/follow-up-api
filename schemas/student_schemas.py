from datetime import date
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, constr, Field

class StudentIn(BaseModel):
    contractor_id: UUID
    instructor_id: Optional[UUID]
    fullname: str
    birthday: Optional[date]
    avatar: Optional[str]
    

class StudentOut(BaseModel):
    id: UUID
    contractor_id: UUID
    instructor_id: Optional[UUID]
    fullname: str
    birthday: Optional[date]
    avatar: Optional[str]

    class Config:
        orm_mode = True