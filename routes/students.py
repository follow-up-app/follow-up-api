from datetime import timedelta
from typing import List
from uuid import UUID
from sqlalchemy import or_
from fastapi import APIRouter, Depends, HTTPException, File
from fastapi.security import OAuth2PasswordRequestForm
from itsdangerous import URLSafeTimedSerializer
from sqlalchemy.orm import Session
from starlette import status
from starlette.background import BackgroundTasks
from config import get_settings, Settings
from core.security import check_is_admin_user
from db import get_db
from db.models import Student, User, Contractor, StatusContract, Status, ResponsibleContract, AddressContract
from schemas.student_schemas import StudentIn, StudentOut, AddressContractorOut, AddressContractorIn, ResponsibleContractIn, ResponsibleContractOut
from fastapi.responses import FileResponse

router = APIRouter()

tags: str = "Student"


@router.post('/', summary='create student', response_model=StudentOut, tags=[tags])
async def create(student_in: StudentIn, current_user: User = Depends(check_is_admin_user), session: Session = Depends(get_db)):
    contract = Contractor(
        company_id=current_user.company_id,
        status=StatusContract.IN_PREPARATION
    )
    session.add(contract)
    session.commit()

    student = Student(
        contractor_id=contract.id,
        fullname=student_in.fullname,
        birthday=student_in.birthday,
        allergy=student_in.allergy,
        genere=student_in.genere,
        document=student_in.document,
        indentity_number=student_in.indentity_number,
        org_exp=student_in.org_exp,
        uf_exp=student_in.uf_exp,
        nationality=student_in.nationality,
        email=student_in.email,
        phone=student_in.phone,
        avatar=student_in.avatar,
        informations=student_in.informations,
        status=Status.ACTIVE
    )
    session.add(student)
    session.commit()

    return StudentOut.from_orm(student)


@router.get('/', summary='Returns all students list', response_model=List[StudentOut], tags=[tags])
async def get_all(current_user: User = Depends(check_is_admin_user), session: Session = Depends(get_db)):
    all_itens = Student.query(session).all()
    return [StudentOut.from_orm(x) for x in all_itens]


@router.get('/{id}', summary='Returns student', tags=[tags])
async def get_id(id: UUID, current_user: User = Depends(check_is_admin_user), session: Session = Depends(get_db)):
    student: Student = Student.query(session).filter(Student.id == id).first()
    if not student:
        raise HTTPException(status_code=404, detail='route not found')

    return StudentOut.from_orm(student)


@router.put('/{id}', summary='Update student', response_model=StudentOut, tags=[tags])
async def update(id: UUID, student_in: StudentIn, current_user: User = Depends(check_is_admin_user), session: Session = Depends(get_db)):
    student: Student = Student.query(session).filter(Student.id == id).first()
    if not student:
        raise HTTPException(status_code=404, detail='route not found')

    student.fullname = student_in.fullname
    student.birthday = student_in.birthday
    student.allergy=student_in.allergy,
    student.genere = student_in.genere
    student.document = student_in.document
    student.indentity_number = student_in.indentity_number
    student.org_exp = student_in.org_exp
    student.uf_exp = student_in.uf_exp
    student.nationality = student_in.nationality
    student.email = student_in.email
    student.phone = student_in.phone
    student.avatar = student_in.avatar
    student.informations = student_in.informations

    session.add(student)
    session.commit()

    return StudentOut.from_orm(student)


@router.get('/{id}/active', summary='active/desactive student', tags=[tags])
async def get_id(id: UUID, current_user: User = Depends(check_is_admin_user), session: Session = Depends(get_db)):
    student: Student = Student.query(session).filter(Student.id == id).first()
    if not student:
        raise HTTPException(status_code=404, detail='route not found')

    if student.status == Status.ACTIVE:
        student.status = Status.INACTIVE
    else:
        student.status = Status.ACTIVE

    session.add(student)
    session.commit()

    return StudentOut.from_orm(student)


@router.post('/{id}/responsable', summary='create responsable', response_model=StudentOut, tags=[tags])
async def create(id: UUID, responsable_in: ResponsibleContractIn, current_user: User = Depends(check_is_admin_user), session: Session = Depends(get_db)):
    student: Student = Student.query(session).filter(Student.id == id).first()
    if not student:
        raise HTTPException(status_code=404, detail='route not found')

    responsable = ResponsibleContract(
        contractor_id=student.contractor_id,
        fullname=responsable_in.fullname,
        birthday=responsable_in.birthday,
        document=responsable_in.document,
        indentity_number=responsable_in.indentity_number,
        org_exp=responsable_in.org_exp,
        uf_exp=responsable_in.uf_exp,
        nationality=responsable_in.nationality,
        email=responsable_in.email,
        phone=responsable_in.phone,
        bond=responsable_in.bond
    )
    session.add(responsable)
    session.commit()

    return StudentOut.from_orm(responsable)


@router.get('/{id}/responsable', summary='Returns all responsable list', response_model=List[ResponsibleContractOut], tags=[tags])
async def get_all(id: UUID, current_user: User = Depends(check_is_admin_user), session: Session = Depends(get_db)):
    student: Student = Student.query(session).filter(Student.id == id).first()
    if not student:
        raise HTTPException(status_code=404, detail='route not found')

    all_itens = ResponsibleContract.query(session).filter(
        ResponsibleContract.contractor_id == student.contractor_id).all()

    return [ResponsibleContractOut.from_orm(x) for x in all_itens]


@router.get('/responsable/{id}', summary='Returns responsables', tags=[tags])
async def get_id(id: UUID, current_user: User = Depends(check_is_admin_user), session: Session = Depends(get_db)):
    responsable: ResponsibleContract = Student.query(
        session).filter(ResponsibleContract.id == id).first()
    if not responsable:
        raise HTTPException(status_code=404, detail='route not found')

    return ResponsibleContractOut.from_orm(responsable)

@router.put('/address/{id}', summary='Update contract address', tags=[tags], response_model=AddressContractorOut)
async def update(id: UUID, responsable_in: ResponsibleContractIn, current_user: User = Depends(check_is_admin_user), session: Session = Depends(get_db)):
    responsable: ResponsibleContract = ResponsibleContract.query(
        session).filter(ResponsibleContract.id == id).first()
    if not responsable:
        raise HTTPException(status_code=404, detail='route not found')

    responsable.fullname = responsable_in.fullname,
    responsable.birthday = responsable_in.birthday
    responsable.document = responsable_in.document
    responsable.indentity_number = responsable_in.indentity_number
    responsable.org_exp = responsable_in.org_exp
    responsable.uf_exp = responsable_in.uf_exp
    responsable.nationality = responsable_in.nationality
    responsable.email = responsable_in.email
    responsable.nationality = responsable_in.nationality
    responsable.phone = responsable_in.phone
    responsable.bond = responsable_in.bond

    session.add(responsable)
    session.commit()

    return ResponsibleContractOut.from_orm(responsable)


@router.delete('/responsable/{id}', summary='Delete responsable', response_model=List[StudentOut], tags=[tags])
async def delete(id: UUID, current_user: User = Depends(check_is_admin_user), session: Session = Depends(get_db)):
    responsable: Student = ResponsibleContract.query(
        session).filter(ResponsibleContract.id == id).first()
    if not responsable:
        raise HTTPException(status_code=404, detail='route not found')
    session.delete(responsable)
    session.commit()


@router.post('/{id}/avatar', summary='Upload avatar', tags=[tags])
async def create(id: UUID, file: bytes = File(...), current_user: User = Depends(check_is_admin_user), session: Session = Depends(get_db)):
    student: Student = Student.query(
        session).filter(Student.id == id).first()
    if not student:
        raise HTTPException(status_code=404, detail='route not found')

    path = 'storage/students/avatar/' + str(student.id) + '.jpg'

    with open(path, 'wb') as f:
        f.write(file)

    student.avatar = path

    session.add(student)
    session.commit()

    return StudentOut.from_orm(student)


@router.get('/avatar/{id}', summary='Returns instructor avatar', tags=[tags])
async def get_id(id: UUID, session: Session = Depends(get_db)):
    student: Student = Student.query(
        session).filter(Student.id == id).first()
    if not student:
        raise HTTPException(status_code=404, detail='route not found')
    
    if student.avatar is None:
        return StudentOut.from_orm(student)

    img = student.avatar

    return FileResponse(img, media_type="image/jpeg")


@router.delete('/{id}/avatar', summary='Upload avatar', tags=[tags])
async def remove(id: UUID, file: bytes = File(...), current_user: User = Depends(check_is_admin_user), session: Session = Depends(get_db)):
    student: Student = Student.query(
        session).filter(Student.id == id).first()
    # if not instructor:
    #     raise HTTPException(status_code=404, detail='route not found')

    # path = 'storage/instructors/avatar/' + str(instructor.id) + '.jpg'

    # with open(path, 'wb') as f:
    #     f.write(file)

    # instructor.avatar = path
    # session.add(instructor)
    # session.commit()

    return StudentOut.from_orm(student)


@router.post('/{id}/address/', summary='Create contract address', response_model=AddressContractorOut, tags=[tags])
async def create(id: UUID, address: AddressContractorIn, current_user: User = Depends(check_is_admin_user), session: Session = Depends(get_db)):
    student: Student = Student.query(
        session).filter(Student.id == id).first()
    if not student:
        raise HTTPException(status_code=404, detail='route not found')

    address = AddressContract(
        contractor_id=student.contractor_id,
        responsible_contract_id=address.responsible_contract_id,
        address=address.address,
        number=address.number,
        complement=address.complement,
        zip_code=address.zip_code,
        district=address.district,
        city=address.city,
        state=address.state,
    )
    session.add(address)
    session.commit()

    return AddressContractorOut.from_orm(address)


@router.get('/{id}/address/', summary='Return contract address', tags=[tags])
async def get_id(id: UUID, current_user: User = Depends(check_is_admin_user), session: Session = Depends(get_db)):
    student: Student = Student.query(
        session).filter(Student.id == id).first()
    if not student:
        raise HTTPException(status_code=404, detail='route not found')

    address: AddressContract = AddressContract.query(
        session).filter(AddressContract.contractor_id)

    return AddressContractorOut.from_orm(address)


@router.put('/address/{id}', summary='Update contract address', tags=[tags], response_model=AddressContractorOut)
async def update(id: UUID, address_in: AddressContractorIn, current_user: User = Depends(check_is_admin_user), session: Session = Depends(get_db)):
    address: AddressContract = AddressContract.query(
        session).filter(AddressContract.id == id).first()
    if not address:
        raise HTTPException(status_code=404, detail='route not found')

    address.responsible_contract_id = address_in.responsible_contract_id,
    address.address = address_in.address
    address.number = address_in.number
    address.complement = address_in.complement
    address.zip_code = address_in.zip_code
    address.district = address_in.district
    address.city = address_in.city
    address.state = address_in.state

    session.add(address)
    session.commit()

    return AddressContractorOut.from_orm(address)
