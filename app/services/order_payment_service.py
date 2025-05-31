from app.repositories.order_payment_repository import OrderPaymentRepository
from app.repositories.instructor_repository import InstructorRepository
from app.repositories.payment_repository import PaymnentRepository
from app.constants.enums.instructor_payments_enum import ModePaymentEnum
from app.constants.enums.payment_enum import PaymentEnum
from datetime import date, timedelta


class OrderPaymentService:
    def __init__(self,
                 order_payment_repository: OrderPaymentRepository,
                 instructor_repository: InstructorRepository,
                 payment_repository: PaymnentRepository
                 ):
        self.order_payment_repository = order_payment_repository
        self.instructor_repository = instructor_repository
        self.payment_repository = payment_repository

    def process_type_fixed(self) -> bool:
        date_due = date.today() + timedelta(days=10)
        instructors = self.instructor_repository.get_by_mode_payment(ModePaymentEnum.MOUNTH)
        for instructor in instructors:
            self.order_payment_repository.create(
                instructor.company_id,
                self.generate_order_number(),
                date_due.strftime("%m-%Y"),
                instructors.value,
                date_due
            )

        return True

    def process_type_scheduled(self) -> bool:
        date_due = date.today() + timedelta(days=10)
        instructors = self.instructor_repository.get_by_mode_payment(ModePaymentEnum.HOUR)
        for instructor in instructors:
            payments = self.payment_repository.get_by_reference_status(
                instructor.id,
                PaymentEnum.CONFIRMED,
                date.today().strftime("%m-%Y"))

            value_total = 0
            for payment in payments:
                value_total += payment.value

            order = self.order_payment_repository.create(
                instructor.company_id,
                self.generate_order_number(),
                date_due.strftime("%m-%Y"),
                value_total,
                date_due
            )

            for payment in payments:
                self.order_payment_repository.create_payment_reference(order.id, payment.id)

        return True

    def process_type_comission(self) -> bool:
        pass

    def generate_order_number(self) -> str:
        number = '000001'
        last_ref = self.order_payment_repository.get_last_order_number()
        if last_ref:
            length = len(number)
            incremented = int(number) + 1

            number = str(incremented).zfill(length)

        return number