from typing import Optional
from uuid import UUID
from pydantic import BaseModel


class SpecialtySchemaIn(BaseModel):
    name: str
    description: Optional[str] = None
    code_nfes: Optional[str] = None
    value_hour: float


class SpecialtySchemaOut(BaseModel):
    id: UUID
    company_id: UUID
    name: str
    description: Optional[str] = None
    code_nfes: Optional[str] = None
    value_hour: float

    class Config:
        orm_mode = True
