from typing import Optional
from uuid import UUID
from pydantic import BaseModel


class AddressInstructorSchemaIn(BaseModel):
    address: str
    number: int
    complement: Optional[str]
    zip_code: str
    district: str
    city: str
    state: str


class AddressInstructorSchemaOut(BaseModel):
    id: UUID
    address: Optional[str]
    number: Optional[int]
    complement: Optional[str]
    zip_code: Optional[str]
    district: Optional[str]
    city: Optional[str]
    state: Optional[str]

    class Config:
        orm_mode = True
