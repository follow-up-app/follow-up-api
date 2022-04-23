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
from db.models import Company, User
from schemas.company_schemas import CompanyIn, CompanyOut


router = APIRouter()

tags: str = "Company"

@router.post('/', summary='Create company', response_model=List[CompanyOut], tags=[tags])
async def create(company_in: CompanyIn, current_user: User = Depends(check_is_admin_user), session: Session=Depends(get_db)):
    company: Company = Company(**company_in.dict())
    session.add(company)
    session.commit()
    return CompanyOut.from_orm(company)


@router.get('/', summary='Returns list of companies', response_model=List[CompanyOut], tags=[tags])
async def get_all(current_user: User = Depends(check_is_admin_user), session: Session=Depends(get_db)):
    all_itens = Company.query(session).all()
    return [CompanyOut.from_orm(x) for x in all_itens]
