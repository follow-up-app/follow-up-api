import datetime
from typing import List
from uuid import UUID
from sqlalchemy.orm import Session
from app.constants.enums.payment_enum import PaymentEnum
from app.schemas.payment_schemas import PaymentGroup, PaymentSchemaIn, PaymentSchemaOut
from db.models import Payment, User
from sqlalchemy.sql.functions import func


class PaymnentRepository:
    def __init__(self, session: Session, current_user: User):
        self.session = session
        self.current_user = current_user

    def create(self, company_id: UUID, schedule_id: UUID, instructor_id: UUID, value: float, date_due: datetime.date) -> PaymentSchemaOut:
        payment = Payment(
            company_id=company_id,
            schedule_id=schedule_id,
            instructor_id=instructor_id,
            value=value,
            date_due=date_due,
            status=PaymentEnum.OPEN
        )
        self.session.add(payment)
        self.session.commit()

        return payment

    def get_id(self, id: UUID) -> PaymentSchemaOut:
        return Payment.query(self.session).filter(Payment.id == id).first()

    def get_schedule_id(self, schedule_id: UUID) -> PaymentSchemaOut:
        return Payment.query(self.session).filter(Payment.schedule_id == schedule_id).first()

    def update_status(self, payment: Payment, status: PaymentEnum) -> PaymentSchemaOut:
        payment.status = status

        self.session.add(payment)
        self.session.commit()

        return payment

    def get_all(self) -> List[PaymentSchemaOut]:
        return Payment.query(self.session).filter(
            Payment.company_id == self.current_user.company_id,
            Payment.status == PaymentEnum.OPEN
        ).all()

    def update(self, payment: Payment, payment_in: PaymentSchemaIn) -> PaymentSchemaOut:
        payment.value = payment_in.value
        payment.date_due = payment_in.date_due
        payment.date_scheduled = payment_in.date_scheduled
        payment.date_done = payment_in.date_done
        payment.description = payment_in.description
        payment.status = payment_in.status

        self.session.add(payment)
        self.session.commit()

        return payment

    def delete(self, id: UUID) -> bool:
        payment = Payment.query(self.session).filter(Payment.id == id).first()

        self.session.delete(payment)
        self.session.commit()

        return True

    def get_filters(self, start: datetime, end: datetime, instructor_id: UUID, status: PaymentEnum) -> List[PaymentSchemaOut]:
        payments = Payment.query(self.session).filter(
            Payment.company_id == self.current_user.company_id,
            Payment.date_due >= start,
            Payment.date_due <= end,
        ).order_by(Payment.date_due.asc()).all()

        if status is not None:
            payment = payment.filter(Payment.status == status)

        if instructor_id is not None:
            payment = payment.filter(Payment.instructor_id == instructor_id)

        return payments

    def get_resume(self, start: datetime, end: datetime, status: PaymentEnum) -> List[PaymentGroup]:
        payments = Payment.query(self.session).filter(
            Payment.company_id == self.current_user.company_id,
            Payment.date_due >= start,
            Payment.date_due <= end,
            Payment.status == status,
            func.count(Payment.instructor_id).label('count'),
            func.sum(Payment.value).label('total')
        ).group_by(Payment.instructor_id).order_by(Payment.date_due.asc()).all()

        if status is not None:
            payment = payment.filter(Payment.status == status)

        return payments
