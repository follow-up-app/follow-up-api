from core.security import hash_password
from uuid import UUID
from typing import Optional
from pydantic import BaseModel
from db.models import UserPermission, Status


class UserStoreIn(BaseModel):
    company_id: UUID
    fullname: str
    email: str
    permission: UserPermission
    document: str
    position: Optional[str]


class UserRegisterSchemaIn(BaseModel):
    fullname: str
    email: str
    document: str
    position: Optional[str]


class LoginSchemaIn(BaseModel):
    username: str
    password: str


class LoginSchemaOut(BaseModel):
    access_token: str
    token_type: str
    expires_in: int


class RecoveryPasswordSchemaIn(BaseModel):
    email: str


class RecoveryPasswordSchemaOut(BaseModel):
    message: str


class ResetPasswordSchemaIn(BaseModel):
    password: str
    token: Optional[str]


class ResetPasswordSchemaOut(BaseModel):
    message: str


class UserOut(BaseModel):
    id: UUID
    fullname: str
    email: str
    permission: UserPermission
    document: str
    image_path: Optional[str]
    position: Optional[str]
    status: Optional[Status]

    class Config:
        orm_mode = True
