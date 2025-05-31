from uuid import UUID
from sqlalchemy.orm import Session
from app.schemas.instructor_payment_schema import InstructorPaymentSchemaIn, InstructorPaymentSchemaOut
from db.models import IntructorPaymentsDetail


class InstructorPaymentRepository:
    def __init__(self, session: Session):
        self.session = session

    def create_payment_details(self, instructor_id: UUID, instructor_payment_in: InstructorPaymentSchemaIn) -> InstructorPaymentSchemaOut:
        instructor_bank = IntructorPaymentsDetail(
            instructor_id=instructor_id,
            key=instructor_payment_in.key
        )
        self.session.add(instructor_bank)
        self.session.commit()

        return instructor_bank

    def get_payment_details(self, instructor_id: UUID) -> InstructorPaymentSchemaIn:
        return IntructorPaymentsDetail.query(self.session).filter(IntructorPaymentsDetail.instructor_id == instructor_id).first()

    def update_payment_details(self, intructor_payment_details: IntructorPaymentsDetail, instructor_payment_in: InstructorPaymentSchemaIn) -> InstructorPaymentSchemaIn:
        intructor_payment_details.key = instructor_payment_in.key

        self.session.add(intructor_payment_details)
        self.session.commit()

        return intructor_payment_details
