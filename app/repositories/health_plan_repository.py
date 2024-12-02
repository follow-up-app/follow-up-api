from sqlalchemy.orm import Session
from db.models import HealthPlan, User
from uuid import UUID
from typing import List
from app.schemas.health_plan_schemas import HealthPlanSchemaIn, HealthPlanSchemaOut


class HealthPlanRepository:
    def __init__(self, session: Session, current_user: User):
        self.session = session
        self.current_user = current_user

    def create(self, health_plan_in: HealthPlanSchemaIn) -> HealthPlanSchemaOut:
        plan = HealthPlan(
            company_id=self.current_user.company_id,
            social_name=health_plan_in.social_name,
            fantasy_name=health_plan_in.fantasy_name,
            document=health_plan_in.document,
            address=health_plan_in.address,
            number_address=health_plan_in.number_address,
            complement=health_plan_in.complement,
            zip_code=health_plan_in.zip_code,
            city=health_plan_in.city,
            state=health_plan_in.state,
            country=health_plan_in.country,
            email=health_plan_in.email,
            phone=health_plan_in.phone,
            active=True
        )

        self.session.add(plan)
        self.session.commit()

        return plan

    def get_all(self) -> List[HealthPlanSchemaOut]:
        return HealthPlan.query(self.session).filter(HealthPlan.company_id == self.current_user.company_id).all()

    def get_id(self, id: UUID) -> HealthPlanSchemaOut:
        return HealthPlan.query(self.session).filter(HealthPlan.id == id).first()

    def update(self, health_plan: HealthPlan, health_plan_in: HealthPlanSchemaIn) -> HealthPlanSchemaOut:
        health_plan.social_name = health_plan_in.social_name
        health_plan.fantasy_name = health_plan_in.fantasy_name
        health_plan.document = health_plan_in.document
        health_plan.address = health_plan_in.address
        health_plan.number_address = health_plan_in.number_address
        health_plan.complement = health_plan_in.complement
        health_plan.city = health_plan_in.city
        health_plan.state = health_plan_in.state
        health_plan.country = health_plan_in.country
        health_plan.email = health_plan_in.email
        health_plan.phone = health_plan_in.phone
        health_plan.active = health_plan_in.active

        self.session.add(health_plan)
        self.session.commit()

        return health_plan

    def remove(self, id: UUID) -> bool:
        health_plan = HealthPlan.query(self.session).filter(
            HealthPlan.id == id).first()

        self.session.delete(health_plan)
        self.session.commit()

        return True

    def get_document(self, document: str) -> HealthPlanSchemaOut:
        return HealthPlan.query(self.session).filter(HealthPlan.document == document).first()
