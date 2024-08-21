
from typing import List
from uuid import UUID
from sqlalchemy.orm import Session
from app.constants.enums.status_enum import StatusEnum
from app.schemas.student_schemas import Filters, StudentSchemaIn, StudentSchemaOut
from db.models import Contractor, Student, User


class StudentRepository:
    def __init__(self, session: Session, current_user: User):
        self.session = session
        self.current_user = current_user

    def create(self, student_in: StudentSchemaIn, contractor_id: UUID) -> StudentSchemaOut:
        student = Student(
            contractor_id=contractor_id,
            fullname=student_in.fullname,
            birthday=student_in.birthday,
            allergy=student_in.allergy,
            genere=student_in.genere,
            document=student_in.document,
            indentity_number=student_in.indentity_number,
            org_exp=student_in.org_exp,
            uf_exp=student_in.uf_exp,
            nationality=student_in.nationality,
            email=student_in.email,
            phone=student_in.phone,
            informations=student_in.informations,
            status=StatusEnum.ACTIVE
        )

        self.session.add(student)
        self.session.commit()

        return student

    def get_id(self, id: UUID) -> StudentSchemaOut:
        return Student.query(self.session).filter(Student.id == id).first()

    def get_all(self) -> List[StudentSchemaOut]:
        return Student.query(self.session).join(Student.contractor).filter(Contractor.company_id == self.current_user.company_id).order_by(Student.fullname.asc()).all()

    def get_all_actives(self) -> List[StudentSchemaOut]:
        return Student.query(self.session).join(Student.contractor).filter(Contractor.company_id == self.current_user.company_id, Student.status == StatusEnum.ACTIVE).order_by(Student.fullname.asc()).all()

    def get_document(self, document: str) -> StudentSchemaOut:
        return Student.query(self.session).filter(Student.document == document).first()

    def active(self, student: Student) -> StudentSchemaOut:
        student.status = StatusEnum.ACTIVE

        self.session.add(student)
        self.session.commit()

        return student

    def inactive(self, student: Student) -> StudentSchemaOut:
        student.status = StatusEnum.INACTIVE

        self.session.add(student)
        self.session.commit()

        return student

    def update(self, student: Student, student_in: StudentSchemaIn) -> StudentSchemaOut:
        student.fullname = student_in.fullname
        student.birthday = student_in.birthday
        student.allergy = student_in.allergy
        student.genere = student_in.genere
        student.document = student_in.document
        student.indentity_number = student_in.indentity_number
        student.org_exp = student_in.org_exp
        student.uf_exp = student_in.uf_exp
        student.nationality = student_in.nationality
        student.email = student_in.email
        student.phone = student_in.phone
        student.informations = student_in.informations

        self.session.add(student)
        self.session.commit()

        return student

    def save_avatar(self, student: Student, path: str) -> StudentSchemaOut:
        student.avatar = path

        self.session.add(student)
        self.session.commit()

        return student

    def get_filters(self, filters_in: Filters) -> List[StudentSchemaOut]:
        return Student.query(self.session).filter(Student.id == filters_in.student_id).order_by(Student.fullname.asc()).all()
