import os
from typing import List
from app.constants.enums.permission_enum import PermissionEnum
from app.constants.enums.status_enum import StatusEnum
from app.repositories.user_repository import UserRepository
from app.schemas.user_schemas import UserSchemaIn, PasswordSchemaIn, UserSchemaOut
from app.core.mailer import Mailer
from app.constants.exceptions.user_exceptions import UserDocumentAlreadyExistsError, UserEmailNotFoundError, UserNotFoundError, UserEmailDocumentAlreadyExistsError
from uuid import UUID
from app.core.crypt import Crypt


class UserService:
    def __init__(self, user_repository: UserRepository, mailer: Mailer):
        self.user_repository = user_repository
        self.mailer = mailer

    def create(self, user_in: UserSchemaIn) -> UserSchemaOut:
        check_document = self.user_repository.get_document(user_in.document)
        if check_document:
            raise ValueError(UserDocumentAlreadyExistsError.MESSAGE)

        check_email = self.user_repository.get_email(user_in.email)
        if check_email:
            raise ValueError(UserEmailDocumentAlreadyExistsError.MESSAGE)

        user = self.user_repository.create(user_in)
        self.mailer.welcome_user(user)

        return user

    def get_all(self) -> List[UserSchemaOut]:
        return self.user_repository.get_all()

    def get_id(self, id: UUID) -> UserSchemaOut:
        return self.user_repository.get_id(id)

    def update(self, id: UUID, user_in: UserSchemaIn) -> UserSchemaOut:
        user = self.user_repository.get_id(id)
        if not user:
            raise ValueError(UserNotFoundError.MESSAGE)

        return self.user_repository.update(user, user_in)

    def recovery_password(self, email: str) -> UserSchemaOut:
        user = self.user_repository.get_email(email)
        if not user:
            raise ValueError(UserNotFoundError)

        self.mailer.recovery_password(user)

        return user

    def refresh_password(self, password: PasswordSchemaIn) -> UserSchemaOut:
        decrypt = Crypt.decrypt(password.token)
        user = self.user_repository.get_id(decrypt[1])
        if not user:
            raise ValueError(UserNotFoundError.MESSAGE)

        return self.user_repository.update_password(user, password)

    def update_password(self, id: UUID, password: PasswordSchemaIn) -> UserSchemaOut:
        user = self.user_repository.get_id(id)
        if not user:
            raise ValueError(UserNotFoundError.MESSAGE)

        return self.user_repository.update_password(user, password)

    def save_avatar(self, id: UUID, file: bytes) -> UserSchemaOut:
        user = self.user_repository.get_id(id)
        if not user:
            raise ValueError(UserNotFoundError.MESSAGE)

        path = 'public/avatars/users/' + str(user.id) + '.jpg'
        if user.image_path != None:
            os.remove(path)

        with open(path, 'wb') as f:
            f.write(file)

        if user.permission == PermissionEnum.INSTRUCTOR:
            instructor_path = 'public/avatars/instructors/' + \
                str(user.id) + '.jpg'
            with open(instructor_path, 'wb') as f:
                f.write(file)

        return self.user_repository.save_avatar(user, path)

    def update_active(self, id: UUID) -> UserSchemaOut:
        user = self.user_repository.get_id(id)
        if not user:
            raise ValueError(UserNotFoundError.MESSAGE)

        if user.status == StatusEnum.ACTIVE:
            return self.user_repository.inactive(user)

        if user.status == StatusEnum.INACTIVE:
            return self.user_repository.active(user)

        return self.user_repository.active(user)

    def inactive(self, id: UUID) -> UserSchemaOut:
        user = self.user_repository.get_id(id)
        if not user:
            raise ValueError(UserNotFoundError.MESSAGE)

        return self.user_repository.inactive(user)

    def avatar(self, id: UUID):
        user = self.user_repository.get_id(id)
        if not user:
            raise ValueError(UserNotFoundError.MESSAGE)

        return user.image_path
