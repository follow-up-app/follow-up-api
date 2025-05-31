import datetime
from typing import List
from uuid import UUID
from sqlalchemy.orm import Session
from db.models import OrderPayment, User, PaymentReference
from app.constants.enums.payment_enum import OrderPaymentEnum
from app.schemas.order_payment_schemas import OrderPaymentSchemaOut, OrderPaymentSchemaIn


class OrderPaymentRepository:
    def __init__(self, session: Session, current_user: User):
        self.session = session,
        self.current_user = current_user

    def create(self, company_id: UUID, number: str, reference: str, value: float, date_due: datetime.date) -> OrderPaymentSchemaOut:
        order = OrderPayment(
            company_id=company_id,
            number=number,
            period_reference=reference,
            value=value,
            date_due=date_due,
            status=OrderPaymentEnum
        )

        self.session.add(order)
        self.session.commit()

        return order

    def get_id(self, id: UUID) -> OrderPaymentSchemaOut:
        return OrderPayment.query(self.session).filter(OrderPayment.id == id).first()

    def get_all(self) -> List[OrderPaymentSchemaOut]:
        return OrderPayment.query(self.session).filter(OrderPayment.company_id == self.current_user.company_id).all()

    def update_status(self, order: OrderPayment, status: OrderPaymentEnum) -> OrderPaymentSchemaOut:
        order.status = status

        self.session.add(order)
        self.session.commit()

        return order

    def update(self, order: OrderPayment, order_in: OrderPaymentSchemaIn) -> OrderPaymentSchemaOut:
        order.period_reference = order_in.period_reference
        order.description = order_in.description
        order.value = order_in.value
        order.date_due = order_in.date_due
        order.date_done = order_in.date_done

        self.session.add(order)
        self.session.commit()

        return order

    def delete(self, id: UUID) -> bool:
        order = self.get_id(id)

        self.session.delete(order)
        self.session.commit()

        return True

    def get_last_order_number(self) -> OrderPaymentSchemaOut:
        return OrderPayment.query(self.session).order_by(OrderPayment.created_date.desc()).first()

    def create_payment_reference(self, id: UUID, payment_id: UUID) -> bool:
        ref = PaymentReference(
            order_payment_id=id,
            payment_id = payment_id
            )

        self.session.add(ref)
        self.session.commit()

        return True

    def delete_payment_reference(self, payment_reference_id: UUID) -> bool:
        ref = PaymentReference.query(self.session).filter(PaymentReference.id == payment_reference_id).first()

        self.session.delete(ref)
        self.session.commit()

        return True

    def get_payment_reference(self, id: UUID, payment_id: UUID):
        return PaymentReference.query(self.session).filter(
            PaymentReference.order_payment_id == id,
            PaymentReference.payment_id == payment_id).all()