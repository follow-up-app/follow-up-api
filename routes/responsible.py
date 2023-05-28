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
from db.models import ResponsibleContract, User, AddressContract
from schemas.contractor_schemas import ResponsibleContractIn, ResponsibleContractOut, AddressContractIn, AddressContractOut
from schemas.student_schemas import StudentIn, StudentOut

router = APIRouter()

tags: str = "Responsible"


@router.get('/', summary='Returns all responsible list', response_model=List[ResponsibleContractOut], tags=[tags])
async def get_all(current_user: User = Depends(check_is_admin_user), session: Session = Depends(get_db)):
    all_itens = ResponsibleContract.query(session).all()
    return [StudentOut.from_orm(x) for x in all_itens]

@router.get('/{id}', summary='Returns responsible', tags=[tags])
async def get_id(id: UUID, current_user: User = Depends(check_is_admin_user), session: Session = Depends(get_db)):
    responsible: ResponsibleContract = ResponsibleContract.query(session).filter(ResponsibleContract.id == id).first()
    if not responsible:
        raise HTTPException(status_code=404, detail='route not found')

    return ResponsibleContractOut.from_orm(responsible)


@router.put('/{id}', summary='Update responsible', response_model=ResponsibleContractOut, tags=[tags])
async def update(id: UUID, responsible_in: ResponsibleContractIn, current_user: User = Depends(check_is_admin_user), session: Session = Depends(get_db)):
    responsible: ResponsibleContract = ResponsibleContract.query(session).filter(ResponsibleContract.id == id).first()
    if not responsible:
        raise HTTPException(status_code=404, detail='route not found')

    responsible.fullname = responsible_in.fullname
    responsible.document = responsible_in.document
    responsible.indentity_number = responsible_in.indentity_number
    responsible.email = responsible_in.email

    session.add(responsible)
    session.commit()

    return StudentOut.from_orm(responsible)

@router.delete('/{id}', summary='Delete responsible in contract', tags=[tags])
async def create(current_user: User = Depends(check_is_admin_user), session: Session = Depends(get_db)):
    responsible: ResponsibleContract = ResponsibleContract.query(session).filter(ResponsibleContract.id == id).first()
    if not responsible:
        raise HTTPException(status_code=404, detail='route not found')
    session.delete(responsible)
    session.commit()


@router.post('/{id}/address', summary='Create address of responsible in contract', tags=[tags])
async def create(address_in: AddressContractOut, current_user: User = Depends(check_is_admin_user), session: Session = Depends(get_db)):
    responsible: ResponsibleContract = ResponsibleContract.query(session).filter(ResponsibleContract.id == id).first()
    if not responsible:
        raise HTTPException(status_code=404, detail='route not found')
    
    address = ResponsibleContract(
        responsible_contract_id = responsible.id,
        address = address_in.address,
        complement = address_in.complement,
        zip_code = address_in.zip_code,
        district = address_in.district,
        city = address_in.city,
        state = address_in.state,
    )
    session.add(address)
    session.commit()

    return ResponsibleContractOut.from_orm(address)

@router.get('/{id}/address', summary='Create address of responsible in contract', response_model=List[AddressContractOut], tags=[tags])
async def create(current_user: User = Depends(check_is_admin_user), session: Session = Depends(get_db)):
    all_itens = AddressContract.query(session).filter(AddressContractOut.responsible_contract_id == id).all()
    return [AddressContractOut.from_orm(x) for x in all_itens]