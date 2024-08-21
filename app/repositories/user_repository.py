from typing import List
from sqlalchemy.orm import Session
from app.constants.enums.permission_enum import PermissionEnum
from app.constants.enums.status_enum import StatusEnum
from db.models import User
from app.schemas.user_schemas import UserSchemaIn, PasswordSchemaIn, UserSchemaOut
from app.core.security import hash_password
import random
import string
from uuid import UUID


class UserRepository:
    def __init__(self, session: Session, current_user: User):
        self.session = session
        self.current_user = current_user

    def create(self, user_in: UserSchemaIn) -> UserSchemaOut:
        user = User(
            company_id=self.current_user.company_id,
            fullname=user_in.fullname,
            password_hash=hash_password(random.choice(string.ascii_uppercase)),
            email=user_in.email.lower(),
            document=user_in.document,
            permission=PermissionEnum.ADMIN,
            position=user_in.position.upper(),
            status=StatusEnum.ACTIVE
        )
        self.session.add(user)
        self.session.commit()

        return user

    def get_id(self, id: UUID) -> UserSchemaOut:
        return User.query(self.session).filter(User.id == id).first()

    def get_all(self) -> List[UserSchemaOut]:
        return User.query(self.session).filter(User.company_id == self.current_user.company_id).order_by(User.fullname.asc()).all()

    def update(self, user: User, user_in: UserSchemaIn) -> UserSchemaOut:
        user.fullname = user_in.fullname
        user.email = user_in.email.lower()
        user.position = user_in.position.upper()

        self.session.add(user)
        self.session.commit()

        return user

    def get_document(self, document: str) -> UserSchemaOut:
        return User.query(self.session).filter(User.document == document).first()

    def get_email(self, email: str) -> UserSchemaOut:
        return User.query(self.session).filter(User.email == email).first()

    def save_avatar(self, user: User, path: str) -> UserSchemaOut:
        user.image_path = path

        self.session.add(user)
        self.session.commit()

        return user

    def active(self, user: User) -> UserSchemaOut:
        user.status = StatusEnum.ACTIVE

        self.session.add(user)
        self.session.commit()

        return user

    def inactive(self, user: User) -> UserSchemaOut:
        user.status = StatusEnum.INACTIVE

        self.session.add(user)
        self.session.commit()

        return user

    def update_password(self, user: User, password: PasswordSchemaIn) -> UserSchemaOut:
        user.password_hash = hash_password(password.password)

        self.session.add(user)
        self.session.commit()
