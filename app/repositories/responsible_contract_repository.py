from typing import List
from uuid import UUID
from sqlalchemy.orm import Session
from app.schemas.responsible_contract_schemas import ResponsibleContractSchemaIn, ResponsibleContractSchemaOut
from db.models import Student, User, ResponsibleContract


class ResponsibleContractRepository:
    def __init__(self, session: Session, current_user: User):
        self.session = session
        self.current_user = current_user

    def create(self, reponsible_contract_in: ResponsibleContractSchemaIn, contractor_id: UUID) -> ResponsibleContractSchemaOut:
        responsible_contract = ResponsibleContract(
            contractor_id=contractor_id,
            fullname=reponsible_contract_in.fullname,
            birthday=reponsible_contract_in.birthday,
            document=reponsible_contract_in.document,
            indentity_number=reponsible_contract_in.indentity_number,
            org_exp=reponsible_contract_in.org_exp,
            uf_exp=reponsible_contract_in.uf_exp,
            nationality=reponsible_contract_in.nationality,
            email=reponsible_contract_in.email,
            phone=reponsible_contract_in.phone,
            bond=reponsible_contract_in.bond,
            main_contract=reponsible_contract_in.main_contract,
        )

        self.session.add(responsible_contract)
        self.session.commit()

        return responsible_contract

    def get_id(self, id: UUID) -> ResponsibleContractSchemaOut:
        return ResponsibleContract.query(self.session).filter(ResponsibleContract.id == id).first()
    
    def get_contractor_id(self, contractor_id: UUID) -> List[ResponsibleContractSchemaOut]:
        return ResponsibleContract.query(self.session).filter(ResponsibleContract.contractor_id == contractor_id).all()

    def get_all(self):
        return ResponsibleContract.query(self.session).filter(ResponsibleContract.company_id == self.current_user.company_id).all()

    def update(self, responsible_contract: ResponsibleContract, reponsible_contract_in: ResponsibleContractSchemaIn) -> ResponsibleContractSchemaOut:
        responsible_contract.fullname = reponsible_contract_in.fullname
        responsible_contract.birthday = reponsible_contract_in.birthday
        responsible_contract.document = reponsible_contract_in.document
        responsible_contract.indentity_number = reponsible_contract_in.indentity_number
        responsible_contract.document = reponsible_contract_in.document
        responsible_contract.indentity_number = reponsible_contract_in.indentity_number
        responsible_contract.org_exp = reponsible_contract_in.org_exp
        responsible_contract.uf_exp = reponsible_contract_in.uf_exp
        responsible_contract.nationality = reponsible_contract_in.nationality
        responsible_contract.email = reponsible_contract_in.email
        responsible_contract.phone = reponsible_contract_in.phone

        self.session.add(responsible_contract)
        self.session.commit()

        return responsible_contract

    def remove(self, id: UUID) -> bool:
        responsible_contract = ResponsibleContract.query(
            self.session).filter(ResponsibleContract.id == id).first()

        self.session.delete(responsible_contract)
        self.session.commit()

        return True
