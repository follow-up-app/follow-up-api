from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.security import check_is_admin_user, hash_password
from db import get_db
from db.models import User, Instructor, UserPermission, StatusInstructor, StatusBankAccount
from schemas.instructor_schema import InstructorOut, InstructorIn

router = APIRouter()

tags: str = "Instructors"


@router.post('/', summary='Create instructor', response_model=InstructorOut, tags=[tags])
async def create(instructor_in: InstructorIn, current_user: User = Depends(check_is_admin_user), session: Session = Depends(get_db)):
    password = '123'
    user = User(
        company_id=current_user.company_id,
        fullname=instructor_in.fullname,
        password_hash=hash_password(password),
        email=instructor_in.email,
        document=instructor_in.document,
        permission=UserPermission.INSTRUCTOR
    )
    session.add(user)

    instructor = Instructor(
        company_id=current_user.company_id,
        user_id = user.id,
        specialty_instructor_id = instructor_in.specialty,
        fullname = instructor_in.fullname,
        email = instructor_in.email,
        phone = instructor_in.phone,
        document = instructor_in.document,
        indentity_number = instructor_in.indentity_number,
        org_exp = instructor_in.org_exp,
        uf_exp = instructor_in.uf_exp,
        nationality=instructor_in.nationality,
        birthday=instructor_in.birthday,
        social_name=instructor_in.social_name,
        fantasy_name=instructor_in.fantasy_name,
        status=StatusInstructor.ACTIVE
    )
    session.add(instructor)
    session.commit()

    return InstructorOut.from_orm(instructor)


@router.post('/{id}/address', summary='Create instructor address', response_model=InstructorOut, tags=[tags])
async def create(instructor_in: InstructorIn, current_user: User = Depends(check_is_admin_user), session: Session = Depends(get_db)):
    password = '123'
    user = User(
        company_id=current_user.company_id,
        fullname=instructor_in.fullname,
        password_hash=hash_password(password),
        email=instructor_in.email,
        document=instructor_in.document,
        permission=UserPermission.INSTRUCTOR
    )
    session.add(user)

    instructor = Instructor(
        company_id=current_user.company_id,
        user_id = user.id,
        specialty_instructor_id = instructor_in.speciality,
        fullname = instructor_in.fullname,
        email = instructor_in.email,
        document = instructor_in.document,
        indentity_number = instructor_in.indentity_number,
        nationality=instructor_in.nationality,
        birthday=instructor_in.birthday,
        social_name=instructor_in.social_name,
        fantasy_name=instructor_in.fantasy_name,
        status=StatusInstructor.ACTIVE
    )
    session.add(instructor)
    session.commit()

    return InstructorOut.from_orm(instructor)



@router.get('/', summary='Returns instructors list', response_model=List[InstructorOut], tags=[tags])
async def get_all(current_user: User = Depends(check_is_admin_user), session: Session = Depends(get_db)):
    all_itens = Instructor.query(session).all()
    return [InstructorOut.from_orm(x) for x in all_itens]


@router.get('/{id}', summary='Returns instructor', tags=[tags])
async def get_id(id: UUID, current_user: User = Depends(check_is_admin_user), session: Session = Depends(get_db)):
    instructor: Instructor = Instructor.query(session).filter(Instructor.id == id).first()
    if not instructor:
        raise HTTPException(status_code=404, detail='route not found')

    return InstructorOut.from_orm(instructor)


@router.put('/{id}', summary='Update program', tags=[tags], response_model=InstructorOut)
async def update(id: UUID, instructor_in: InstructorIn, current_user: User = Depends(check_is_admin_user), session: Session = Depends(get_db)):
    instructor: Instructor = Instructor.query(session).filter(Instructor.id == id).first()
    if not instructor:
        raise HTTPException(status_code=404, detail='route not found')

    user: User = User.query(session).filter(User.id == instructor.user_id).first()
    
    instructor.social_name=instructor_in.social_name
    instructor.fantasy_name=instructor_in.fantasy_name
    instructor.fullname=instructor_in.fullname
    instructor.document=instructor_in.document
    instructor.address=instructor_in.address
    instructor.district=instructor_in.district
    instructor.city=instructor_in.city
    instructor.state=instructor_in.state
    instructor.email=instructor_in.email
    instructor.speciality=instructor_in.speciality
    instructor.value_hour=instructor_in.value_hour

    user.email = instructor_in.email
    user.document = instructor_in.document
    user.fullname = instructor_in.fullname
        
    session.add(instructor)
    session.add(user)
    session.commit()

    return InstructorOut.from_orm(instructor)

@router.delete('/{id}', summary='Delete instuctor', response_model=List[InstructorOut], tags=[tags])
async def delete(id: UUID, current_user: User = Depends(check_is_admin_user), session: Session = Depends(get_db)):
    instructor: Instructor = Instructor.query(session).filter(Instructor.id == id).first()
    if not instructor:
        raise HTTPException(status_code=404, detail='route not found')
    session.delete(instructor)
    session.commit()
