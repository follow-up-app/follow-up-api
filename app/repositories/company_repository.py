from typing import List
from sqlalchemy.orm import Session
from app.constants.enums.company_enum import CompanyEnum
from db.models import Company, User
from app.schemas.company_schemas import CompanySchemaIn, CompanySchemaOut
from uuid import UUID


class CompanyRepository:
    def __init__(self, session: Session, current_user: User):
        self.session = session
        self.current_user = current_user

    def create(self, company_in: CompanySchemaIn) -> CompanySchemaOut:
        company = Company(
            name=company_in.name.upper(),
            document=company_in.document,
            address=company_in.address,
            number_address=company_in.number_address,
            complement=company_in.complement,
            zip_code=company_in.zip_code,
            city=company_in.city,
            state=company_in.state,
            country=company_in.country,
            email=company_in.email.lower(),
            phone=company_in.phone,
            city_code=company_in.city_code,
            aliquot=company_in.aliquot,
            item_list_service=company_in.item_list_service,
            municipal_tax_code=company_in.municipal_tax_code,
            status=CompanyEnum.ACTIVE
        )
        self.session.add(company)
        self.session.commit()

        return company

    def get_id(self, id: UUID) -> CompanySchemaOut:
        return Company.query(self.session).filter(Company.id == id).first()

    def get_all(self) -> List[CompanySchemaOut]:
        return Company.query(self.session).order_by(Company.name.asc()).all()

    def update(self, company: Company, company_in: CompanySchemaIn) -> CompanySchemaOut:
        company.name = company_in.name.upper()
        company.address = company_in.address
        company.number_address = company_in.number_address
        company.complement = company_in.complement
        company.zip_code = company_in.zip_code
        company.city = company_in.city
        company.state = company_in.state
        company.country = company_in.country
        company.email = company_in.email.lower()
        company.phone = company_in.phone
        company.city_code = company_in.city_code
        company.item_list_service = company_in.item_list_service
        company.municipal_tax_code = company_in.municipal_tax_code
        company.status = company_in.status

        self.session.add(company)
        self.session.commit()

        return company

    def get_document(self, document: str) -> CompanySchemaOut:
        return Company.query(self.session).filter(Company.document == document).first()

    def company_by_user_logged(self)-> CompanySchemaOut:
        return Company.query(self.session).filter(Company.id == self.current_user.company_id).first()