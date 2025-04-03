from typing import List
from app.repositories.company_repository import CompanyRepository
from app.schemas.company_schemas import CompanySchemaIn, CompanySchemaOut
from app.constants.exceptions.company_exceptions import CompanyDocumentAlreadyExistsError, CompanyNotFoundError
from uuid import UUID


class CompanyService:
    def __init__(self, company_repository: CompanyRepository):
        self.company_repository = company_repository

    def create(self,  company_in: CompanySchemaIn) -> CompanySchemaOut:
        company_check = self.company_repository.get_document(
            company_in.document)
        if company_check:
            raise ValueError(CompanyDocumentAlreadyExistsError.MESSAGE)

        return self.company_repository.create(company_in)

    def get_all(self) -> List[CompanySchemaOut]:
        return self.company_repository.get_all()

    def get_id(self, id: UUID) -> CompanySchemaOut:
        return self.company_repository.get_id(id)

    def update(self, id: UUID, company_in: CompanySchemaIn) -> CompanySchemaOut:
        company = self.company_repository.get_id(id)
        if not company:
            raise ValueError(CompanyNotFoundError.MESSAGE)

        return self.company_repository.update(company, company_in)

    def get_document(self, document: str) -> CompanySchemaOut:
        return self.company_repository.get_document(document)

    def get_company_by_user_logged(self) -> CompanySchemaOut:
        return self.company_repository.company_by_user_logged()