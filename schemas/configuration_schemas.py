from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, constr, Field

class SpecialtyIn(BaseModel):
    specialty: Optional[str]

class SpecialtyOut(BaseModel):
    id: UUID
    company_id: UUID
    specialty: Optional[str]

    class Config:
        orm_mode = True