from typing import List
from uuid import UUID
from sqlalchemy.orm import Session
from app.schemas.address_contract_schemas import AddressContractorSchemaIn, AddressContractorSchemaOut
from db.models import AddressContract, User


class AndressContractRepository:
    def __init__(self, session: Session, current_user: User):
        self.session = session
        self.current_user = current_user

    def create(self, address_in: AddressContractorSchemaIn, contractor_id: UUID) -> AddressContractorSchemaOut:
        address = AddressContract(
            contractor_id=contractor_id,
            responsible_contract_id=address_in.responsible_contract_id,
            address=address_in.address,
            number=address_in.number,
            complement=address_in.complement,
            zip_code=address_in.zip_code,
            district=address_in.district,
            city=address_in.city,
            state=address_in.state,
        )
        self.session.add(address)
        self.session.commit()

        return address

    def get_id(self, id: UUID) -> AddressContractorSchemaOut:
        return AddressContract.query(self.session).filter(AddressContract.id == id).first()

    def get_all(self) -> List[AddressContractorSchemaOut]:
        return AddressContract.query(self.session).filter(AddressContract.company_id == self.current_user.company_id).all()
    
    def get_contractor_id(self, contractor_id: UUID) -> AddressContractorSchemaOut:
        return AddressContract.query(self.session).filter(AddressContract.contractor_id == contractor_id).first()

    def update(self, address: AddressContract, address_in: AddressContractorSchemaIn) -> AddressContractorSchemaOut:
        address.address = address_in.address
        address.number = address_in.number
        address.complement = address_in.complement
        address.zip_code = address_in.zip_code
        address.district = address_in.district
        address.city = address_in.city

        self.session.add(address)
        self.session.commit()

        return address

    def remove(self, id: UUID) -> bool:
        address = AddressContract.query(
            self.session).filter(AddressContract.id == id).first()

        self.session.delete(address)
        self.session.commit()

        return True
