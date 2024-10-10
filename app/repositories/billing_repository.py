import datetime
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
from db.models import Billing, User, Student, StudentPlan, Plan
from app.constants.enums.billing_enum import BillingEnum
from app.schemas.billing_schemas import BillingSchemaIn, BillingSchemaOut, BillingGroup
from sqlalchemy.sql.functions import func
from app.constants.enums.billing_enum import CategoryEnum


class BillingRepository:
    def __init__(self, session: Session, current_user: User):
        self.session = session
        self.current_user = current_user

    def create(self, company_id: UUID, schedule_id: UUID, student_id: UUID, category: CategoryEnum,  value: float, date_due: datetime.date, reference: str) -> BillingSchemaOut:
        billing = Billing(
            company_id=company_id,
            schedule_id=schedule_id,
            instructor_id=student_id,
            category=category,
            value=value,
            date_due=date_due,
            reference=reference,
            status=BillingEnum.OPEN
        )
        self.session.add(billing)
        self.session.commit()

        return billing

    def get_id(self, id: UUID) -> BillingSchemaOut:
        return Billing.query(self.session).filter(Billing.id == id).first()

    def get_schedule_id(self, schedule_id: UUID) -> BillingSchemaOut:
        return Billing.query(self.session).filter(Billing.schedule_id == schedule_id).first()

    def get_all(self) -> List[BillingSchemaOut]:
        return Billing.query(self.session).filter(
            Billing.company_id == self.current_user.company_id,
            Billing.status == BillingEnum.OPEN
        ).all()

    def update(self, billing: Billing, billing_in: BillingSchemaIn) -> BillingSchemaOut:
        billing.value = billing_in.value
        billing.date_due = billing_in.date_due
        billing.date_done = billing_in.date_done
        billing.status = billing_in.status

        self.session.add(billing)
        self.session.commit()

        return billing

    def update_status(self, billing: Billing, status: BillingEnum) -> BillingSchemaOut:
        billing.status = status

        self.session.add(billing)
        self.session.commit()

        return billing

    def delete(self, id: UUID) -> bool:
        billing = Billing.query(self.session).filter(Billing.id == id).first()

        self.session.delete(billing)
        self.session.commit()

        return True

    def delete_for_schedule(self, schedule_id: UUID) -> bool:
        billing = Billing.query(self.session).filter(
            Billing.schedule_id == schedule_id).first()

        self.session.delete(billing)
        self.session.commit()

        return True

    def get_resume(self, start: datetime, end: datetime, status: BillingEnum, student_id: UUID) -> List[BillingGroup]:
        query = (
            self.session.query(
                Billing.student_id,
                Student.fullname,
                Plan.social_name,
                Billing.status,
                func.count(Billing.student_id).label('count'),
                func.sum(Billing.value).label('total'),
            )
            .join(Student, Billing.student_id == Student.id)
            .leftJoin(StudentPlan, Student.student_id == StudentPlan.student_id)
            .leftJoin(Plan, StudentPlan.plan_id == Plan.id)
            .filter(
                Billing.company_id == self.current_user.company_id,
                Billing.date_due >= start,
                Billing.date_due <= end,
                Billing.status == status
            )
        )

        if student_id:
            query = query.filter(Billing.instructor_id == student_id)

        billings = query.group_by(
            Billing.student_id,
            Student.fullname,
            Plan.social_name,
            Billing.status).all()

        return billings

    def get_student_status(self, start: datetime, end: datetime, status: BillingEnum, student_id: UUID) -> List[BillingSchemaOut]:
        return Billing.query(self.session).filter(
            Billing.date_due >= start,
            Billing.date_due <= end,
            Billing.student_id == student_id,
            Billing.status == status
        ).all()

    def get_filters(self, start: datetime, end: datetime, student_id: UUID, status: BillingEnum) -> List[BillingSchemaOut]:
        billings = Billing.query(self.session).filter(
            Billing.company_id == self.current_user.company_id,
            Billing.date_due >= start,
            Billing.date_due <= end,
        ).order_by(Billing.date_due.asc()).all()

        if status is not None:
            billings = billings.filter(Billing.status == status)

        if student_id is not None:
            billings = billings.filter(Billing.student_id == student_id)

        return billings
