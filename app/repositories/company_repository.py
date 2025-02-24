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
            social_name=company_in.social_name.upper(),
            fantasy_name=company_in.fantasy_name.upper(),
            document=company_in.document,
            address=company_in.address,
            number_address=company_in.number_address,
            complement=company_in.complement,
            zip_code=company_in.zip_code,
            district=company_in.district,
            city=company_in.city,
            state=company_in.state,
            email=company_in.email.lower(),
            phone=company_in.phone,
            city_code=company_in.city_code,
            aliquot=company_in.aliquot,
            municipal_registration=company_in.municipal_registration,
            item_list_service=company_in.item_list_service,
            municipal_tax_code=company_in.municipal_tax_code,
            iss_retained=company_in.iss_retained,
            licences_n=company_in.licences_n,
            api_nfes_token=company_in.api_nfes_token,
            status=CompanyEnum.ACTIVE,
        )
        self.session.add(company)
        self.session.commit()

        return company

    def get_id(self, id: UUID) -> CompanySchemaOut:
        return Company.query(self.session).filter(Company.id == id).first()

    def get_all(self) -> List[CompanySchemaOut]:
        return Company.query(self.session).order_by(Company.name.asc()).all()

    def update(self, company: Company, company_in: CompanySchemaIn) -> CompanySchemaOut:
        company.social_name = company_in.social_name.upper()
        company.fantasy_name = company_in.fantasy_name.upper()
        company.address = company_in.address
        company.number_address = company_in.number_address
        company.complement = company_in.complement
        company.zip_code = company_in.zip_code
        company.district = company_in.district
        company.city = company_in.city
        company.state = company_in.state
        company.email = company_in.email.lower()
        company.phone = company_in.phone
        company.city_code = company_in.city_code
        company.municipal_registration = company_in.municipal_registration
        company.item_list_service = company_in.item_list_service
        company.municipal_tax_code = company_in.municipal_tax_code
        company.iss_retained = company_in.iss_retained
        company.licences_n = company_in.licences_n
        company.api_nfes_token = company_in.api_nfes_token
        company.status = company_in.status

        self.session.add(company)
        self.session.commit()

        return company

    def get_document(self, document: str) -> CompanySchemaOut:
        return Company.query(self.session).filter(Company.document == document).first()

    def company_by_user_logged(self) -> CompanySchemaOut:
        return (
            Company.query(self.session)
            .filter(Company.id == self.current_user.company_id)
            .first()
        )
