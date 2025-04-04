from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.security import get_current_user, check_is_ower_user
from db import get_db
from app.schemas.company_schemas import CompanySchemaIn, CompanySchemaOut
import logging
from app.services.company_service import CompanyService
from app.repositories.company_repository import CompanyRepository
from db.models import User


router = APIRouter()

tags: str = "Company"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_service(session: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    company_repository = CompanyRepository(session, current_user)
    return CompanyService(company_repository)


@router.post('/', summary='Create company', response_model=CompanySchemaOut, tags=[tags])
async def create(company_in: CompanySchemaIn, company_service: CompanyService = Depends(get_service)):
    try:
        company = company_service.create(company_in)
        return CompanySchemaOut.from_orm(company)

    except Exception as e:
        logger.error(f"Error in create company: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.get('/', summary='Return companies list', response_model=List[CompanySchemaOut], tags=[tags])
async def get_all(company_service: CompanyService = Depends(get_service), current_user: User = Depends(check_is_ower_user)):
    try:
        companies = company_service.get_all()
        return [CompanySchemaOut.from_orm(x) for x in companies]

    except Exception as e:
        logger.error(f"Error in query company: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.get('/{id}', summary='Return company for id', response_model=CompanySchemaOut, tags=[tags])
async def get_id(id: UUID, company_service: CompanyService = Depends(get_service)):
    try:
        company = company_service.get_id(id)
        return CompanySchemaOut.from_orm(company)

    except Exception as e:
        logger.error(f"Error in query company for id: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.patch('/{id}', summary='Update company', response_model=CompanySchemaOut, tags=[tags])
async def update(id: UUID, company_in: CompanySchemaIn, company_service: CompanyService = Depends(get_service), current_user: User = Depends(check_is_ower_user)):
    try:
        company = company_service.update(id, company_in)
        return CompanySchemaOut.from_orm(company)

    except Exception as e:
        logger.error(f"Error in update company: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.get('/document/{document}', summary='Returns company for document', response_model=List[CompanySchemaOut], tags=[tags])
async def get_document(document: str, company_service: CompanyService = Depends(get_service)):
    try:
        company = company_service.get_document(document)
        return [CompanySchemaOut.from_orm(company)]

    except Exception as e:
        logger.error(f"Error in query company for document: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.get('/user/logged', summary='Return company for user logged', response_model=CompanySchemaOut, tags=[tags])
async def get_id(company_service: CompanyService = Depends(get_service)):
    try:
        company = company_service.get_company_by_user_logged()
        return CompanySchemaOut.from_orm(company)

    except Exception as e:
        logger.error(f"Error in query company for user-logged: {e}")
        raise HTTPException(status_code=400, detail=str(e))