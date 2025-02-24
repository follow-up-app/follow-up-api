from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.services.billing_service import BillingService
from app.core.security import get_current_user
from app.repositories.billing_repository import BillingRepository
from app.schemas.billing_schemas import BillingSchemaIn, BillingSchemaOut, BillingFilters, ManyBillingUpdate
from db import get_db
from db.models import User
import logging

router = APIRouter()

tags: str = "Billing"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_service(session: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    billing_repository = BillingRepository(session, current_user)
    return BillingService(billing_repository)


@router.get('/', summary='Return all billings', response_model=List[BillingSchemaOut], tags=[tags])
async def get_all(billing_service: BillingService = Depends(get_service)):
    try:
        billings = billing_service.get_all()
        return [BillingSchemaOut.from_orm(x) for x in billings]

    except Exception as e:
        logger.error(f"Error in query billings: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.get('/{id}', summary='Return billing', response_model=BillingSchemaOut, tags=[tags])
async def get_id(id: UUID, billing_service: BillingService = Depends(get_service)):
    try:
        billing = billing_service.get_id(id)
        return BillingSchemaOut.from_orm(billing)

    except Exception as e:
        logger.error(f"Error in query billing: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.patch('/{id}', summary='Update billing', response_model=BillingSchemaOut, tags=[tags])
async def update(id: UUID, billing_in: BillingSchemaIn, billing_service: BillingService = Depends(get_service)):
    try:
        billing = billing_service.update(id, billing_in)
        return BillingSchemaOut.from_orm(billing)

    except Exception as e:
        logger.error(f"Error in update billing: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.post('/filters/', summary='Return billings filtered', response_model=List[BillingSchemaOut], tags=[tags])
async def get_filters(filters_in: BillingFilters, billing_service: BillingService = Depends(get_service)):
    try:
        billings = billing_service.get_filters(filters_in)
        return [BillingSchemaOut.from_orm(x) for x in billings]

    except Exception as e:
        logger.error(f"Error in query billings filtered: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.post('/resume', summary='Return resume billings', tags=[tags])
async def get_resume(filters_in: BillingFilters, billing_service: BillingService = Depends(get_service)):
    try:
        billings = billing_service.get_resume(filters_in)
        return [
            {
                "student_id": billing.student_id,
                "fullname": billing.fullname,
                "category": billing.category,
                "status": billing.status,
                "count": billing.count,
                "total": billing.total,
            }
            for billing in billings
        ]

    except Exception as e:
        logger.error(f"Error in resume query in resume billings: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.post('/for-student', summary='Return all billings for instructors', response_model=List[BillingSchemaOut], tags=[tags])
async def get_student_status(filters_in: BillingFilters, billing_service: BillingService = Depends(get_service)):
    try:
        billings = billing_service.get_student_status(filters_in)
        return [BillingSchemaOut.from_orm(x) for x in billings]

    except Exception as e:
        logger.error(f"Error in resume query billings for student: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.post('/many-change-status', summary='Change status in many billings', tags=[tags])
async def get_student_status(billing_in: ManyBillingUpdate, billing_service: BillingService = Depends(get_service)):
    try:
        return billing_service.update_many_status(billing_in.ids, billing_in.status)

    except Exception as e:
        logger.error(f"Error in change status in many billings: {e}")
        raise HTTPException(status_code=400, detail=str(e))
