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

tags: str = "Address responsibles"

@router.get('/{id}', summary='Address details', response_model=List[AddressContractOut], tags=[tags])
async def create(current_user: User = Depends(check_is_admin_user), session: Session = Depends(get_db)):
    address = AddressContract.query(session).filter(AddressContractOut.id == id).all()
    if not address:
        raise HTTPException(status_code=404, detail='route not found')

    return ResponsibleContractOut.from_orm(address)

@router.put('/{id}', summary='Update address of responsible in contract', response_model=AddressContractOut, tags=[tags])
async def create(address_in: AddressContractOut, current_user: User = Depends(check_is_admin_user), session: Session = Depends(get_db)):
    address:AddressContract = AddressContract.query(session).filter(AddressContractOut.id == id).all()
    if not address:
        raise HTTPException(status_code=404, detail='route not found')

    address.address = address_in.address
    address.complement = address_in.complement
    address.zip_code = address_in.zip_code
    address.district = address_in.district
    address.city = address_in.city
    address.state = address_in.state  
    session.add(address)
    session.commit()

    return ResponsibleContractOut.from_orm(address)




@router.delete('/{id}', summary='Delete address', tags=[tags])
async def delete(id: UUID, current_user: User = Depends(check_is_admin_user), session: Session = Depends(get_db)):
    address = AddressContract.query(session).filter(AddressContractOut.id == id).all()
    if not address:
        raise HTTPException(status_code=404, detail='route not found')
    session.delete(address)
    session.commit()