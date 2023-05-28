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
from config import get_settings, Settings
from core.security import check_is_admin_user, hash_password, verify_password, create_access_token, get_current_user
from db import get_db
from db.models import Student, User, UserPermission, Contractor, StatusContract, ResponsibleContract
from schemas.contractor_schemas import ContractorIn, ContractorOut, ResponsibleContractIn, ResponsibleContractOut
from schemas.student_schemas import StudentIn, StudentOut


router = APIRouter()

tags: str = "Contracts"

@router.post('/', summary='Create conctract', response_model=ResponsibleContractOut, tags=[tags])
async def create(contract_in: ContractorIn, current_user: User = Depends(check_is_admin_user), session: Session = Depends(get_db)):
    contract = Contractor(
        status = StatusContract.ACTIVE 
    )
    session.add(contract)

    responsible = ResponsibleContract(
        contractor_id = contract.id,
        fullname = contract_in.fullname,
        document = contract_in.document,
        indentity_number = contract_in.indentity_number,
        email = contract_in.email,
    )
    session.add(responsible)
    session.commit()

    return ResponsibleContractOut.from_orm(responsible)


@router.get('/', summary='Returns contractor list', response_model=List[ContractorOut], tags=[tags])
async def get_all(current_user: User = Depends(check_is_admin_user), session: Session = Depends(get_db)):
    all_itens = Contractor.query(session).all()
    return [ContractorOut.from_orm(x) for x in all_itens]


@router.get('/{id}', summary='Returns contact details', tags=[tags])
async def get_id(id: UUID, current_user: User = Depends(check_is_admin_user), session: Session = Depends(get_db)):
    contract: Contractor = Contractor.query(session).filter(Contractor.id == id).first()
    if not contract:
        raise HTTPException(status_code=404, detail='route not found')

    return ContractorOut.from_orm(contract)


@router.get('/{id}/responsible', summary='Returns contractor list of contract', response_model=List[ResponsibleContractOut], tags=[tags])
async def get_all(current_user: User = Depends(check_is_admin_user), session: Session = Depends(get_db)):
    all_itens = ResponsibleContract.query(session).filter(ResponsibleContract.contractor_id == id).all()
    return [ResponsibleContractOut.from_orm(x) for x in all_itens]


@router.post('/{id}/responsible', summary='Create responsible in contract', response_model=List[ResponsibleContractOut], tags=[tags])
async def create(contract_in: ContractorIn, current_user: User = Depends(check_is_admin_user), session: Session = Depends(get_db)):
    contract: Contractor = Contractor.query(session).filter(Contractor.id == id).first()
    if not contract:
        raise HTTPException(status_code=404, detail='route not found')
    
    responsible = ResponsibleContract(
        contractor_id = contract.id,
        fullname = contract_in.fullname,
        document = contract_in.document,
        indentity_number = contract_in.indentity_number,
        email = contract_in.email,
    )
    session.add(responsible)
    session.commit()

    return ResponsibleContractOut.from_orm(responsible)

   

@router.post('/{id}/student', summary='Create student in contract', response_model=List[ResponsibleContractOut], tags=[tags])
async def create(student_in: StudentIn, current_user: User = Depends(check_is_admin_user), session: Session = Depends(get_db)):
    contract: Contractor = Contractor.query(session).filter(Contractor.id == id).first()
    if not contract:
        raise HTTPException(status_code=404, detail='route not found')
    
    student = Student(
        contractor_id = contract.id,
        fullname = student_in.fullname,
        birthday = student_in.birthday,
        avatar = student_in.avatar,
    )
    session.add(student)
    session.commit()

    return StudentOut.from_orm(student)


@router.get('/{id}/student', summary='Returns students list of contract', response_model=List[StudentOut], tags=[tags])
async def get_all(current_user: User = Depends(check_is_admin_user), session: Session = Depends(get_db)):
    all_itens = Student.query(session).filter(StudentOut.contractor_id == id).all()
    return [ResponsibleContractOut.from_orm(x) for x in all_itens]