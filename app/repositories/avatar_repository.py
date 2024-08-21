from uuid import UUID
from sqlalchemy.orm import Session
from db.models import Student, User


class AvatarRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_path_student_avatar(self, id: UUID):
        student = Student.query(self.session).filter(Student.id == id).first()
        return student.avatar
    
    def get_path_user_avatar(self, id: UUID):
        user = User.query(self.session).filter(User.id == id).first()
        return user.image_path
