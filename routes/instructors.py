from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, File
from sqlalchemy.orm import Session
from core.security import check_is_admin_user, hash_password, get_current_user
from db import get_db
from db.models import User, Instructor, UserPermission, Status, AddressInctructor
from schemas.instructor_schema import InstructorOut, InstructorIn, AddressInstructorOut, AddressInstructorIn, Filters
import re
from fastapi.responses import FileResponse

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
        permission=UserPermission.INSTRUCTOR,
        position='APLICADOR',
        status=Status.ACTIVE
    )
    session.add(user)
    session.commit()

    instructor = Instructor(
        company_id=current_user.company_id,
        user_id=user.id,
        # specialty_instructor_id=instructor_in.specialty,
        fullname=instructor_in.fullname,
        email=instructor_in.email,
        phone=instructor_in.phone,
        document=instructor_in.document,
        indentity_number=instructor_in.indentity_number,
        org_exp=instructor_in.org_exp,
        uf_exp=instructor_in.uf_exp,
        nationality=instructor_in.nationality,
        birthday=instructor_in.birthday,
        document_company=instructor_in.document_company,
        social_name=instructor_in.social_name,
        fantasy_name=instructor_in.fantasy_name,
        status=Status.ACTIVE
    )
    session.add(instructor)
    session.commit()

    return InstructorOut.from_orm(instructor)


@router.get('/', summary='Return instructors list', response_model=List[InstructorOut], tags=[tags])
async def get_all(current_user: User = Depends(check_is_admin_user), session: Session = Depends(get_db)):
    all_itens = Instructor.query(session).all()
    return [InstructorOut.from_orm(x) for x in all_itens]


@router.get('/{id}', summary='Return instructor', tags=[tags])
async def get_id(id: UUID, current_user: User = Depends(check_is_admin_user), session: Session = Depends(get_db)):
    instructor: Instructor = Instructor.query(
        session).filter(Instructor.id == id).first()
    if not instructor:
        raise HTTPException(status_code=404, detail='route not found')

    return InstructorOut.from_orm(instructor)


@router.put('/{id}', summary='Update instructor', tags=[tags], response_model=InstructorOut)
async def update(id: UUID, instructor_in: InstructorIn, current_user: User = Depends(check_is_admin_user), session: Session = Depends(get_db)):
    instructor: Instructor = Instructor.query(
        session).filter(Instructor.id == id).first()
    if not instructor:
        raise HTTPException(status_code=404, detail='instructor not found')
    
    user: User = User.query(session).filter(User.id == instructor.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail='user not found')
    
    user.fullname = instructor_in.fullname
    user.document = instructor_in.document
    user.email = instructor_in.email

    session.add(user)
    session.commit()
    
    instructor.fullname = instructor_in.fullname
    # instructor.specialty_instructor_id = instructor.specialty_instructor_id
    instructor.document = instructor_in.document
    instructor.email = instructor_in.email
    instructor.phone = instructor_in.phone
    instructor.indentity_number = instructor_in.indentity_number
    instructor.org_exp = instructor_in.org_exp
    instructor.uf_exp = instructor_in.uf_exp
    instructor.nationality = instructor_in.nationality
    instructor.birthday = instructor_in.birthday
    instructor.document_company = instructor_in.document_company
    instructor.social_name = instructor_in.social_name
    instructor.fantasy_name = instructor_in.fantasy_name

    session.add(instructor)
    session.commit()

    return InstructorOut.from_orm(instructor)


@router.post('/{id}/avatar', summary='Upload avatar', tags=[tags])
async def create(id: UUID, file: bytes = File(...), current_user: User = Depends(check_is_admin_user), session: Session = Depends(get_db)):
    instructor: Instructor = Instructor.query(
        session).filter(Instructor.id == id).first()
    if not instructor:
        raise HTTPException(status_code=404, detail='route not found')

    user: User = User.query(
        session).filter(User.id == instructor.user_id).first()

    path = 'storage/instructors/avatar/' + str(instructor.id) + '.jpg'

    with open(path, 'wb') as f:
        f.write(file)

    instructor.avatar = path
    user.image_path = path

    session.add(instructor)
    session.add(user)
    session.commit()

    return InstructorOut.from_orm(instructor)


@router.get('/avatar/{id}', summary='Returns instructor avatar', tags=[tags])
async def get_id(id: UUID, session: Session = Depends(get_db)):
    instructor: Instructor = Instructor.query(
        session).filter(Instructor.id == id).first()
    if not instructor:
        raise HTTPException(status_code=404, detail='route not found')

    if instructor.avatar is None:
        return InstructorOut.from_orm(instructor)

    img = instructor.avatar

    return FileResponse(img, media_type="image/jpeg")


@router.delete('/{id}/avatar', summary='Upload avatar', tags=[tags])
async def remove(id: UUID, file: bytes = File(...), current_user: User = Depends(check_is_admin_user), session: Session = Depends(get_db)):
    instructor: Instructor = Instructor.query(
        session).filter(Instructor.id == id).first()
    # if not instructor:
    #     raise HTTPException(status_code=404, detail='route not found')

    # path = 'storage/instructors/avatar/' + str(instructor.id) + '.jpg'

    # with open(path, 'wb') as f:
    #     f.write(file)

    # instructor.avatar = path
    # session.add(instructor)
    # session.commit()

    return InstructorOut.from_orm(instructor)


@router.post('/{id}/address/', summary='Create instructor address', response_model=AddressInstructorOut, tags=[tags])
async def create(id: UUID, instructor_in: AddressInstructorIn, current_user: User = Depends(check_is_admin_user), session: Session = Depends(get_db)):
    instructor: Instructor = Instructor.query(
        session).filter(Instructor.id == id).first()
    if not instructor:
        raise HTTPException(status_code=404, detail='route not found')

    instructor_address = AddressInctructor(
        instructor_id=instructor.id,
        address=instructor_in.address,
        number=instructor_in.number,
        complement=instructor_in.complement,
        zip_code=instructor_in.zip_code,
        district=instructor_in.district,
        city=instructor_in.city,
        state=instructor_in.state,
    )
    session.add(instructor_address)
    session.commit()

    return AddressInstructorOut.from_orm(instructor_address)


@router.get('/{id}/address/', summary='Returns instructor address', tags=[tags])
async def get_id(id: UUID, current_user: User = Depends(check_is_admin_user), session: Session = Depends(get_db)):
    address_instructor: AddressInctructor = AddressInctructor.query(
        session).filter(AddressInctructor.instructor_id == id).first()
    if not address_instructor:
        raise HTTPException(status_code=404, detail='route not found')

    return AddressInstructorOut.from_orm(address_instructor)


@router.put('/address/{id}', summary='Update instructor address', tags=[tags], response_model=AddressInstructorOut)
async def update(id: UUID, instructor_in: AddressInstructorIn, current_user: User = Depends(check_is_admin_user), session: Session = Depends(get_db)):
    address_instructor: AddressInctructor = AddressInctructor.query(
        session).filter(AddressInctructor.id == id).first()
    if not address_instructor:
        raise HTTPException(status_code=404, detail='route not found')

    address_instructor.address = instructor_in.address
    address_instructor.number = instructor_in.number
    address_instructor.complement = instructor_in.complement
    address_instructor.zip_code = instructor_in.zip_code
    address_instructor.district = instructor_in.district
    address_instructor.city = instructor_in.city
    address_instructor.state = instructor_in.state

    session.add(address_instructor)
    session.commit()

    return AddressInstructorOut.from_orm(address_instructor)


@router.delete('/{id}', summary='Delete instuctor',  tags=[tags])
async def delete(id: UUID, current_user: User = Depends(check_is_admin_user), session: Session = Depends(get_db)):
    instructor: Instructor = Instructor.query(
        session).filter(Instructor.id == id).first()
    if not instructor:
        raise HTTPException(status_code=404, detail='route not found')
    session.delete(instructor)
    session.commit()


@router.get('/{id}/active', summary='active/desactive student', tags=[tags])
async def get_id(id: UUID, current_user: User = Depends(check_is_admin_user), session: Session = Depends(get_db)):
    instructor: Instructor = Instructor.query(
        session).filter(Instructor.id == id).first()
    if not instructor:
        raise HTTPException(status_code=404, detail='route not found')

    if instructor.status == Status.ACTIVE:
        instructor.status = Status.INACTIVE
    else:
        instructor.status = Status.ACTIVE

    session.add(instructor)
    session.commit()

    return InstructorOut.from_orm(instructor)


@router.post('/filters', summary='Return list with filters', tags=[tags])
async def get_filters(filters: Filters, current_user: User = Depends(get_current_user), session: Session = Depends(get_db)):
    all_itens = Instructor.query(session).filter(Instructor.id == filters.instructor_id).all()
    return [InstructorOut.from_orm(x) for x in all_itens]
