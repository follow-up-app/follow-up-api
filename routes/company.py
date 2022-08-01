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
from core.security import check_is_admin_user, hash_password, verify_password, create_access_token, get_current_user
from db import get_db
from db.models import Company, StatusCompany, User
from schemas.company_schemas import CompanyIn, CompanyOut


router = APIRouter()

tags: str = "Company"


@router.post('/', summary='Create company', response_model=CompanyOut, tags=[tags])
async def create(company_in: CompanyIn, session: Session = Depends(get_db)):
    company = Company(
        name=company_in.name,
        document=company_in.document,
        address=company_in.address,
        complement=company_in.complement,
        zip_code=company_in.zip_code,
        city=company_in.city,
        state=company_in.state,
        country=company_in.country,
        email=company_in.email,
        phone=company_in.phone,
        status=StatusCompany.ACTIVE
    )
    session.add(company)
    session.commit()

    return CompanyOut.from_orm(company)


@router.get('/', summary='Returns companies list', response_model=List[CompanyOut], tags=[tags])
async def get_all(session: Session = Depends(get_db)):
    all_itens = Company.query(session).all()
    return [CompanyOut.from_orm(x) for x in all_itens]


@router.get('/{id}', summary='Returns company', response_model=List[CompanyOut], tags=[tags])
async def get_id(id: UUID, current_user: User = Depends(check_is_admin_user), session: Session = Depends(get_db)):
    company: Company = Company.query(session).filter(Company.id == id).first()
    if not company:
        raise HTTPException(status_code=404, detail='route not found')

    return [CompanyOut.from_orm(company)]


@router.put('/{id}', summary='Update company', response_model=List[CompanyOut], tags=[tags])
async def update(id: UUID, company_in: CompanyIn, current_user: User = Depends(check_is_admin_user), session: Session = Depends(get_db)):
    company = Company(
        name=company_in.name,
        document=company_in.document,
        address=company_in.address,
        complement=company_in.complement,
        zip_code=company_in.zip_code,
        city=company_in.city,
        state=company_in.state,
        country=company_in.country,
        email=company_in.email,
        phone=company_in.phone,
        status=StatusCompany.ACTIVE
    )
    session.add(company)
    session.commit()

    return CompanyOut.from_orm(company)


@router.delete('/{id}', summary='Delete company', response_model=List[CompanyOut], tags=[tags])
async def delete(id: UUID, current_user: User = Depends(check_is_admin_user), session: Session = Depends(get_db)):
    pass
