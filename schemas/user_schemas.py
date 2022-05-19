from core.security import hash_password
from uuid import UUID

from pydantic import BaseModel, constr, Field

from db.models import UserPermission


class UserRegisterSchemaIn(BaseModel):
    fullname: str
    email: str
    permission: UserPermission
    password: str
    document: str

class UserStoreIn(BaseModel):
    company_id: UUID
    fullname: str
    email: str
    permission: UserPermission
    document: str
    


class LoginSchemaIn(BaseModel):
    username: str
    password: str


class LoginSchemaOut(BaseModel):
    access_token: str
    token_type: str


class RecoveryPasswordSchemaIn(BaseModel):
    email: str


class RecoveryPasswordSchemaOut(BaseModel):
    message: str


class ResetPasswordSchemaIn(BaseModel):
    password: str
    token: str


class ResetPasswordSchemaOut(BaseModel):
    message: str


class UserOut(BaseModel):
    id: UUID
    fullname: constr(max_length=255)
    email: str
    permission: UserPermission

    class Config:
        orm_mode = True