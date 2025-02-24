from uuid import UUID
from typing import Optional
from pydantic import BaseModel
from app.constants.enums.permission_enum import PermissionEnum
from app.constants.enums.status_enum import StatusEnum


class UserSchemaIn(BaseModel):
    company_id: Optional[UUID]
    fullname: str
    email: str
    permission: Optional[PermissionEnum]
    document: str
    position: Optional[str]
    status: Optional[StatusEnum]


class PasswordSchemaIn(BaseModel):
    password: str
    token: Optional[str]


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


class ResetPasswordSchemaIn(BaseModel):
    password: str
    token: Optional[str]


class UserSchemaOut(BaseModel):
    id: UUID
    company_id: UUID
    fullname: str
    email: str
    permission: PermissionEnum
    document: str
    image_path: Optional[str]
    position: Optional[str]
    status: Optional[StatusEnum]

    class Config:
        orm_mode = True
