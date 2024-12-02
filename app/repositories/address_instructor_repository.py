from typing import List
from sqlalchemy.orm import Session
from uuid import UUID
from app.schemas.address_instructor_schemas import AddressInstructorSchemaIn, AddressInstructorSchemaOut
from db.models import AddressInstructor


class AddressInstructorRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, address_in: AddressInstructorSchemaIn, instructor_id: UUID) -> AddressInstructorSchemaOut:
        instructor_address = AddressInstructor(
            instructor_id=instructor_id,
            address=address_in.address,
            number=address_in.number,
            complement=address_in.complement,
            zip_code=address_in.zip_code,
            district=address_in.district,
            city=address_in.city,
            state=address_in.state,
        )
        self.session.add(instructor_address)
        self.session.commit()

        return instructor_address

    def get_id(self, id: UUID) -> AddressInstructorSchemaOut:
        return AddressInstructor.query(self.session).filter(AddressInstructor.id == id).first()

    def get_all(self, instructor_id: UUID) -> List[AddressInstructorSchemaOut]:
        return AddressInstructor.query(self.session).filter(AddressInstructor.instructor_id == instructor_id).all()

    def get_instructor(self, instructor_id: UUID) -> AddressInstructorSchemaOut:
        return AddressInstructor.query(self.session).filter(AddressInstructor.instructor_id == instructor_id).first()

    def update(self, address: AddressInstructor, address_in: AddressInstructorSchemaIn) -> AddressInstructorSchemaOut:
        address.address = address_in.address
        address.number = address_in.number
        address.complement = address_in.complement
        address.zip_code = address_in.zip_code
        address.district = address_in.district
        address.city = address_in.city
        address.state = address_in.state

        self.session.add(address)
        self.session.commit()

        return address

    def remove(self, id: UUID) -> bool:
        address = AddressInstructor.query(
            self.session).filter(AddressInstructor.id == id).first()

        self.session.delete(address)
        self.session.commit()

        return True
