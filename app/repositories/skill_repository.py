from typing import List
from uuid import UUID
from sqlalchemy.orm import Session
from app.schemas.skill_schemas import SkillSchemaIn, SkillSchemaOut
from db.models import Skill, User


class SkillRepository:
    def __init__(self, session: Session, current_user: User):
        self.session = session
        self.current_user = current_user

    def create(self, skill_in: SkillSchemaIn) -> SkillSchemaOut:
        skill = Skill(
            company_id=self.current_user.company_id,
            specialty_id=skill_in.specialty_id,
            name=skill_in.name.upper(),
            objective=skill_in.objective
        )

        self.session.add(skill)
        self.session.commit()

        return skill

    def get_id(self, id: UUID) -> SkillSchemaOut:
        return Skill.query(self.session).filter(Skill.id == id).first()

    def get_all(self) -> List[SkillSchemaOut]:
        return Skill.query(self.session).filter(Skill.company_id == self.current_user.company_id).all()

    def get_speciality(self, specialty_id: UUID) -> List[SkillSchemaOut]:
        return Skill.query(self.session).filter(Skill.specialty_id == specialty_id).all()

    def get_skill_student(self, skill_ids: List[UUID]) -> List[SkillSchemaOut]:
        return Skill.query(self.session).filter(Skill.id.in_(skill_ids)).all()

    def update(self, skill: Skill, skill_in: SkillSchemaIn) -> SkillSchemaOut:
        skill.name = skill_in.name
        skill.specialty_id = skill_in.specialty_id
        skill.objective = skill_in.objective

        self.session.add(skill)
        self.session.commit()

        return skill
