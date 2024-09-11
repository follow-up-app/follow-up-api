from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.security import get_current_user
from app.repositories.instructor_repository import InstructorRepository
from app.repositories.payment_repository import PaymnentRepository
from app.repositories.schedule_repository import ScheduleRepository
from app.schemas.payment_schemas import PaymentFilters, PaymentGroup, PaymentSchemaIn, PaymentSchemaOut
from app.services.payment_service import PaymentService
from db import get_db
from db.models import User
import logging

router = APIRouter()

tags: str = "Payment"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_service(session: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    payment_repository = PaymnentRepository(session, current_user)
    schedule_repository = ScheduleRepository(session, current_user)
    instructor_repository = InstructorRepository(session, current_user)

    return PaymentService(payment_repository, schedule_repository, instructor_repository)


@router.post('/', summary='Create payment', response_model=PaymentSchemaOut, tags=[tags])
async def create(payment_in: PaymentSchemaIn, payment_service: PaymentService = Depends(get_service)):
    try:
        payment = payment_service.create(payment_in)
        return PaymentSchemaOut.from_orm(payment)

    except Exception as e:
        logger.error(f"Error in create payment: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.get('/', summary='Return all payments', response_model=List[PaymentSchemaOut], tags=[tags])
async def get_all(payment_service: PaymentService = Depends(get_service)):
    try:
        payments = payment_service.get_all()
        return [PaymentSchemaOut.from_orm(x) for x in payments]

    except Exception as e:
        logger.error(f"Error in query payments: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.get('/{id}', summary='Return payment', response_model=PaymentSchemaOut, tags=[tags])
async def get_id(id: UUID, payment_service: PaymentService = Depends(get_service)):
    try:
        payment = payment_service.get_id(id)
        return PaymentSchemaOut.from_orm(payment)

    except Exception as e:
        logger.error(f"Error in query payment: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.patch('/{id}', summary='Update payment', response_model=PaymentSchemaOut, tags=[tags])
async def update(id: UUID, payment_in: PaymentSchemaIn, payment_service: PaymentService = Depends(get_service)):
    try:
        payment = payment_service.update(id, payment_in)
        return PaymentSchemaOut.from_orm(payment)

    except Exception as e:
        logger.error(f"Error in update payments: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.delete('/{id}', summary='Delete payment', tags=[tags])
async def delete(id: UUID, payment_service: PaymentService = Depends(get_service)):
    try:
        return payment_service.delete(id)

    except Exception as e:
        logger.error(f"Error in delete payments: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.post('/filters/', summary='Return payments filtered', response_model=List[PaymentSchemaOut], tags=[tags])
async def get_filters(filters_in: PaymentFilters, payment_service: PaymentService = Depends(get_service)):
    try:
        payments = payment_service.get_filters(filters_in)
        return [PaymentSchemaOut.from_orm(x) for x in payments]

    except Exception as e:
        logger.error(f"Error in query payments filtered: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.post('/resume/', summary='Return all payments', response_model=List[PaymentGroup], tags=[tags])
async def get_resume(filters_in: PaymentFilters, payment_service: PaymentService = Depends(get_service)):
    try:
        payments = payment_service.get_resume(filters_in)
        return [PaymentGroup.from_orm(x) for x in payments]

    except Exception as e:
        logger.error(f"Error in resume query payments: {e}")
        raise HTTPException(status_code=400, detail=str(e))
