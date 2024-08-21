from uuid import UUID
from app.repositories.avatar_repository import AvatarRepository


class AvatarService:
    def __init__(self, avatar_repository: AvatarRepository):
        self.avatar_repository = avatar_repository

    def get_path_student_avatar(self, id: UUID):
        return self.avatar_repository.get_path_student_avatar(id)

    def get_path_user_avatar(self, id: UUID):
        return self.avatar_repository.get_path_user_avatar(id)
