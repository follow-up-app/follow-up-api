from typing import List
from uuid import UUID
from sqlalchemy.orm import Session
from app.constants.enums.contract_enum import ContractEnum
from app.schemas.contractor_schemas import ContractorIn, ContractorOut
from db.models import Contractor, User


class ContractorRepository:
    def __init__(self, session: Session, current_user: User):
        self.session = session
        self.current_user = current_user

    def create(self) -> ContractorOut:
        contract = Contractor(
            company_id=self.current_user.company_id,
            status=ContractEnum.ACTIVE
        )

        self.session.add(contract)
        self.session.commit()

        return contract

    def get_id(self, id: UUID) -> ContractorOut:
        return Contractor.query(self.session).filter(Contractor.id == id).first()

    def get_all(self) -> List[ContractorOut]:
        return Contractor.query(self.session).filter(Contractor.company_id == self.current_user.company_id).all()

    def update(self, contractor: Contractor, contractor_in: ContractorIn) -> ContractorOut:
        contractor.status = contractor_in.status

        self.session.add(contractor)
        self.session.commit()

        return contractor
