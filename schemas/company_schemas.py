from uuid import UUID
from pydantic import BaseModel, constr, Field

from db.models import StatusCompany, UserPermission

class CompanyIn(BaseModel):
    name: str
    document: str
    address: str
    complement: str or None
    zip_code: str
    city: str
    state: str
    country: str
    email: str
    phone: str
    status: StatusCompany


class CompanyOut(BaseModel):
    id: UUID
    name: str
    document: str
    address: str
    complement: str or None
    zip_code: str
    city: str
    state: str
    country: str
    email: str
    phone: str
    status: StatusCompany

    class Config:
        orm_mode = True

