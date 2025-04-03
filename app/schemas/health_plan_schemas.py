from typing import Optional
from uuid import UUID
from pydantic import BaseModel


class HealthPlanSchemaIn(BaseModel):
    social_name: str
    fantasy_name: str
    document: str
    address: str
    number: Optional[int]
    complement: Optional[str] = None
    zip_code: str
    district: str
    city: str
    state: str
    country: Optional[str] = None
    email: str
    phone: str


class HealthPlanSchemaOut(BaseModel):
    id: UUID
    social_name: str
    fantasy_name: str
    document: str
    address: str
    number: Optional[int]
    complement: Optional[str] = None
    zip_code: str
    district: Optional[str] = None
    city: str
    state: str
    country: Optional[str] = None
    email: str
    phone: str
    active: bool

    class Config:
        orm_mode = True
