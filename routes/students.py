from datetime import timedelta
from typing import List
from uuid import UUID
from sqlalchemy import or_
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from itsdangerous import URLSafeTimedSerializer
from sqlalchemy.orm import Session
from starlette import status
from starlette.background import BackgroundTasks
import re
import os
import unidecode
from config import get_settings, Settings
from core.security import check_is_admin_user, check_is_parents_user, hash_password, verify_password, create_access_token, get_current_user
from db import get_db
from db.models import Student, User
from schemas.student_schemas import StudentIn, StudentOut


router = APIRouter()

tags: str = "Student"


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
    student.avatar = student_in.avatar

    session.add(student)
    session.commit()

    return StudentOut.from_orm(student)


@router.delete('/{id}', summary='Delete student', response_model=List[StudentOut], tags=[tags])
async def delete(id: UUID, current_user: User = Depends(check_is_parents_user), session: Session = Depends(get_db)):
    student: Student = Student.query(session).filter(Student.id == id).first()
    if not student:
        raise HTTPException(status_code=404, detail='route not found')
    session.delete(student)
    session.commit()
