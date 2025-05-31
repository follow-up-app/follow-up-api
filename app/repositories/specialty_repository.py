from typing import List
from uuid import UUID
from sqlalchemy.orm import Session
from app.schemas.specialty_schemas import SpecialtySchemaIn, SpecialtySchemaOut
from db.models import Specialty, User


class SpecialtyRepository:
    def __init__(self, session: Session, current_user: User):
        self.session = session
        self.current_user = current_user

    def create(self, specialty_in: SpecialtySchemaIn) -> SpecialtySchemaOut:
        specialty = Specialty(
            company_id=self.current_user.company_id,
            name=specialty_in.name.upper(),
            description=specialty_in.description,
            code_nfes=specialty_in.code_nfes,
            value_hour=specialty_in.value_hour,
        )
        self.session.add(specialty)
        self.session.commit()

        return specialty

    def get_id(self, id: UUID) -> SpecialtySchemaOut:
        return Specialty.query(self.session).filter(Specialty.id == id).first()

    def get_all(self) -> List[SpecialtySchemaOut]:
        return Specialty.query(self.session).filter(
            Specialty.company_id == self.current_user.company_id,
        ).all()

    def update(self, specialty: Specialty, specialty_in: SpecialtySchemaIn) -> SpecialtySchemaOut:
        specialty.name = specialty_in.name
        specialty.description = specialty_in.description
        specialty.code_nfes = specialty_in.code_nfes
        specialty.value_hour = specialty_in.value_hour

        self.session.add(specialty)
        self.session.commit()

        return specialty

    def delete(self, id: UUID) -> bool:
        specialty = Specialty.query(self.session).filter(Specialty.id == id).first()

        self.session.delete(specialty)
        self.session.commit()