from typing import List
from uuid import UUID
from app.constants.exceptions.specialty_exceptions import SpecialtyNotFoundError
from app.repositories.specialty_repository import SpecialtyRepository
from app.schemas.specialty_schemas import SpecialtySchemaIn, SpecialtySchemaOut


class SpecialtyService:
    def __init__(self, specialty_repository: SpecialtyRepository) -> None:
        self.specialty_repository = specialty_repository

    def create(self, specialty_in: SpecialtySchemaIn) -> SpecialtySchemaOut:
        return self.specialty_repository.create(specialty_in)

    def get_id(self, id: UUID) -> SpecialtySchemaOut:
        return self.specialty_repository.get_id(id)

    def get_all(self) -> List[SpecialtySchemaOut]:
        return self.specialty_repository.get_all()

    def update(self, id: UUID, specialty_in: SpecialtySchemaIn) -> SpecialtySchemaOut:
        specialty = self.specialty_repository.get_id(id)
        if not specialty:
            raise ValueError(SpecialtyNotFoundError.MESSAGE)

        return self.specialty_repository.update(specialty, specialty_in)

    def delete(self, id: UUID) -> bool:
        return self.specialty_repository.delete(id)
