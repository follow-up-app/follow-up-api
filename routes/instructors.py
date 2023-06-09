from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.security import check_is_admin_user, hash_password
from db import get_db
from db.models import User, Instructor, UserPermission, StatusInstructor, StatusBankAccount, AddressInctructor
from schemas.instructor_schema import InstructorOut, InstructorIn
import re

router = APIRouter()

tags: str = "Instructors"


@router.post('/', summary='Create instructor', response_model=InstructorOut, tags=[tags])
async def create(instructor_in: InstructorIn, current_user: User = Depends(check_is_admin_user), session: Session = Depends(get_db)):
    password = '123'

    mail: User = User.query(session).filter(
        User.email == instructor_in.email).first()
    if mail:
        raise HTTPException(status_code=501, detail='E-mail ja cadastrado')

    instructor: Instructor = Instructor.query(
        session).filter(Instructor.document == re.sub(u'[^a-zA-Z0-9áéíóúÁÉÍÓÚâêîôÂÊÎÔãõÃÕçÇ: ]', '', instructor_in.document)).first()
    if instructor:
        raise HTTPException(status_code=501, detail='Documento ja cadastrado')

    user = User(
        company_id=current_user.company_id,
        fullname=instructor_in.fullname,
        password_hash=hash_password(password),
        email=instructor_in.email,
        document=instructor_in.document,
        permission=UserPermission.INSTRUCTOR
    )
    session.add(user)
    session.commit()

    instructor = Instructor(
        company_id=current_user.company_id,
        user_id=user.id,
        specialty_instructor_id=instructor_in.specialty,
        fullname=instructor_in.fullname,
        email=instructor_in.email,
        phone=re.sub(u'[^a-zA-Z0-9áéíóúÁÉÍÓÚâêîôÂÊÎÔãõÃÕçÇ: ]',
                     '', instructor_in.phone),
        document=re.sub(u'[^a-zA-Z0-9áéíóúÁÉÍÓÚâêîôÂÊÎÔãõÃÕçÇ: ]',
                        '', instructor_in.document),
        indentity_number=instructor_in.indentity_number,
        org_exp=instructor_in.org_exp,
        uf_exp=instructor_in.uf_exp,
        nationality=instructor_in.nationality,
        birthday=instructor_in.birthday,
        document_company=re.sub(
            u'[^a-zA-Z0-9áéíóúÁÉÍÓÚâêîôÂÊÎÔãõÃÕçÇ: ]', '', instructor_in.document_company),
        social_name=instructor_in.social_name,
        fantasy_name=instructor_in.fantasy_name,
        status=StatusInstructor.ACTIVE
    )
    session.add(instructor)
    session.commit()

    instructor_address = AddressInctructor(
        instructor_id=instructor.id,
        address=instructor_in.address.address,
        complement=instructor_in.address.complement,
        zip_code=instructor_in.address.zip_code,
        district=instructor_in.address.district,
        city=instructor_in.address.city,
        state=instructor_in.address.state,
    )
    session.add(instructor_address)
    session.commit()

    return InstructorOut.from_orm(instructor)


@router.get('/', summary='Returns instructors list', response_model=List[InstructorOut], tags=[tags])
async def get_all(current_user: User = Depends(check_is_admin_user), session: Session = Depends(get_db)):
    all_itens = Instructor.query(session).all()
    return [InstructorOut.from_orm(x) for x in all_itens]


@router.get('/{id}', summary='Returns instructor', tags=[tags])
async def get_id(id: UUID, current_user: User = Depends(check_is_admin_user), session: Session = Depends(get_db)):
    instructor: Instructor = Instructor.query(
        session).filter(Instructor.id == id).first()
    if not instructor:
        raise HTTPException(status_code=404, detail='route not found')

    return InstructorOut.from_orm(instructor)


@router.put('/{id}', summary='Update program', tags=[tags], response_model=InstructorOut)
async def update(id: UUID, instructor_in: InstructorIn, current_user: User = Depends(check_is_admin_user), session: Session = Depends(get_db)):
    instructor: Instructor = Instructor.query(
        session).filter(Instructor.id == id).first()
    if not instructor:
        raise HTTPException(status_code=404, detail='route not found')

    instructor.fullname = instructor_in.fullname
    instructor.document = re.sub(u'[^a-zA-Z0-9áéíóúÁÉÍÓÚâêîôÂÊÎÔãõÃÕçÇ: ]',
                                 '', instructor_in.document)
    instructor.email = instructor_in.email
    instructor.phone = re.sub(u'[^a-zA-Z0-9áéíóúÁÉÍÓÚâêîôÂÊÎÔãõÃÕçÇ: ]',
                              '', instructor_in.phone)
    instructor.indentity_number = instructor_in.indentity_number
    instructor.org_exp = instructor_in.org_exp
    instructor.uf_exp = instructor_in.uf_exp
    instructor.nationality = instructor_in.nationality
    instructor.birthday = instructor_in.birthday
    instructor.document_company = re.sub(u'[^a-zA-Z0-9áéíóúÁÉÍÓÚâêîôÂÊÎÔãõÃÕçÇ: ]',
                                         '', instructor_in.document_company)
    instructor.social_name = instructor_in.social_name
    instructor.fantasy_name = instructor_in.fantasy_name
    # instructor.status = instructor_in.status

    address_instructor: AddressInctructor = AddressInctructor.query(session).filter(
        AddressInctructor.instructor_id == instructor.id).first()

    if address_instructor:
        address_instructor.address = instructor_in.address.address
        address_instructor.complement = instructor_in.address.complement
        address_instructor.zip_code = instructor_in.address.zip_code
        address_instructor.district = instructor_in.address.district
        address_instructor.city = instructor_in.address.city
        address_instructor.state = instructor_in.address.state

        session.add(instructor)

    else:
        instructor_address = AddressInctructor(
            instructor_id=instructor.id,
            address=instructor_in.address.address,
            complement=instructor_in.address.complement,
            zip_code=instructor_in.address.zip_code,
            district=instructor_in.address.district,
            city=instructor_in.address.city,
            state=instructor_in.address.state,
        )
        session.add(instructor_address)

    session.commit()

    return InstructorOut.from_orm(instructor)


@router.delete('/{id}', summary='Delete instuctor', response_model=List[InstructorOut], tags=[tags])
async def delete(id: UUID, current_user: User = Depends(check_is_admin_user), session: Session = Depends(get_db)):
    instructor: Instructor = Instructor.query(
        session).filter(Instructor.id == id).first()
    if not instructor:
        raise HTTPException(status_code=404, detail='route not found')
    session.delete(instructor)
    session.commit()
