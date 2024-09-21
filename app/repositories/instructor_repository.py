from typing import List
from uuid import UUID
from sqlalchemy.orm import Session
from app.constants.enums.status_enum import StatusEnum
from app.schemas.instructor_payment_schema import InstructorPaymentSchemaIn
from app.schemas.instructor_schema import Filters, InstructorSchemaIn, InstructorSchemaOut
from db.models import Instructor, User


class InstructorRepository:
    def __init__(self, session: Session, current_user: User):
        self.session = session
        self.current_user = current_user

    def create(self, user_id: UUID, instructor_in: InstructorSchemaIn) -> InstructorSchemaOut:
        instructor = Instructor(
            company_id=self.current_user.company_id,
            user_id=user_id,
            fullname=instructor_in.fullname,
            email=instructor_in.email.lower(),
            phone=instructor_in.phone,
            document=instructor_in.document,
            indentity_number=instructor_in.indentity_number,
            org_exp=instructor_in.org_exp,
            uf_exp=instructor_in.uf_exp,
            nationality=instructor_in.nationality,
            birthday=instructor_in.birthday,
            document_company=instructor_in.document_company,
            social_name=instructor_in.social_name,
            fantasy_name=instructor_in.fantasy_name,
            status=StatusEnum.ACTIVE
        )

        self.session.add(instructor)
        self.session.commit()

        return instructor

    def get_id(self, id: UUID) -> InstructorSchemaOut:
        return Instructor.query(self.session).filter(Instructor.id == id).first()

    def get_all(self) -> List[InstructorSchemaOut]:
        return Instructor.query(self.session).filter(Instructor.company_id == self.current_user.company_id).order_by(Instructor.fullname.asc()).all()

    def get_actives_all(self) -> List[InstructorSchemaOut]:
        return Instructor.query(self.session).filter(Instructor.company_id == self.current_user.company_id, Instructor.status == StatusEnum.ACTIVE).order_by(Instructor.fullname.asc()).all()

    def get_document(self, document: str) -> InstructorSchemaOut:
        return Instructor.query(self.session).filter(Instructor.document == document).first()

    def update(self, instructor: Instructor, instructor_in: InstructorSchemaIn):
        instructor.fullname = instructor_in.fullname
        instructor.document = instructor_in.document
        instructor.email = instructor_in.email.lower()
        instructor.phone = instructor_in.phone
        instructor.indentity_number = instructor_in.indentity_number
        instructor.org_exp = instructor_in.org_exp
        instructor.uf_exp = instructor_in.uf_exp
        instructor.nationality = instructor_in.nationality
        instructor.birthday = instructor_in.birthday

        self.session.add(instructor)
        self.session.commit()

        return instructor

    def save_avatar(self, instructor: Instructor, path: str) -> InstructorSchemaOut:
        instructor.avatar = path

        self.session.add(instructor)
        self.session.commit()

        return instructor

    def active(self, instructor: Instructor) -> InstructorSchemaOut:
        instructor.status = StatusEnum.ACTIVE

        self.session.add(instructor)
        self.session.commit()

        return instructor

    def inactive(self, instructor: Instructor) -> InstructorSchemaOut:
        instructor.status = StatusEnum.INACTIVE

        self.session.add(instructor)
        self.session.commit()

        return instructor

    def get_instructor_user(self) -> InstructorSchemaOut:
        return Instructor.query(self.session).filter(Instructor.user_id == self.current_user.id).first()

    def get_filters(self, filters_in: Filters) -> List[InstructorSchemaOut]:
        return Instructor.query(self.session).filter(Instructor.id == filters_in.instructor_id).order_by(Instructor.fullname.asc()).all()

    def update_type_payment(self, instructor: Instructor, instructor_payment_in: InstructorPaymentSchemaIn):
        instructor.specialty_id = instructor_payment_in.specialty_id
        instructor.type_payment = instructor_payment_in.type_payment
        instructor.mode_payment = instructor_payment_in.mode_payment
        instructor.value = instructor_payment_in.value
        instructor.comission = instructor_payment_in.comission

        self.session.add(instructor)
        self.session.commit()

        return instructor
