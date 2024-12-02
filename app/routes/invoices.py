from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.services.invoice_service import InvoiceService
from app.core.security import get_current_user
from app.repositories.invoice_repository import InvoiceRepository
from app.repositories.company_repository import CompanyRepository
from app.repositories.student_repository import StudentRepository
from app.repositories.billing_repository import BillingRepository
from app.repositories.health_plan_repository import HealthPlanRepository
from app.repositories.responsible_contract_repository import ResponsibleContractRepository
from app.repositories.address_contract_repository import AndressContractRepository
from app.schemas.invoice_schemas import InvoiceSchemaIn, InvoiceSchemaOut, InvoiceBillingSchemaOut
from app.core.invoice_requests import InvoiceRequests
from db import get_db
from db.models import User
import logging

router = APIRouter()

tags: str = "Invoice"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_service(session: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    invoice_requests = InvoiceRequests(current_user.company)
    invoice_repository = InvoiceRepository(session, current_user)
    company_repository = CompanyRepository(session, current_user)
    student_repository = StudentRepository(session, current_user)
    billing_repository = BillingRepository(session, current_user)
    health_plan_repository = HealthPlanRepository(session, current_user)
    responsible_contract_repository = ResponsibleContractRepository(
        session, current_user)
    address_contract_repository = AndressContractRepository(
        session, current_user)

    return InvoiceService(
        company_repositoy=company_repository,
        student_repository=student_repository,
        billing_repository=billing_repository,
        invoice_repository=invoice_repository,
        health_plan_repository=health_plan_repository,
        responsible_repository=responsible_contract_repository,
        address_contract_repository=address_contract_repository,
        invoice_requests=invoice_requests
    )


@router.post('/', summary='sender invoice', response_model=InvoiceSchemaOut, tags=[tags])
async def create(invoice_in: InvoiceSchemaIn, invoice_service: InvoiceService = Depends(get_service)):
    try:
        return invoice_service.sender(invoice_in)

    except Exception as e:
        logger.error(f"Error in sender invoice: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.get('/billing/{billing_id}', summary='Return invoice list by students', response_model=List[InvoiceBillingSchemaOut], tags=[tags])
async def get_all(billing_id: UUID, invoice_service: InvoiceService = Depends(get_service)):
    try:
        invoices = invoice_service.by_billing(billing_id)
        return [InvoiceBillingSchemaOut.from_orm(x) for x in invoices]

    except Exception as e:
        logger.error(f"Error in query invoices billing: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.get('/reference/{reference}', summary='Return invoice for reference', tags=[tags])
async def by_reference(reference: str, invoice_service: InvoiceService = Depends(get_service)):
    try:
        return invoice_service.by_reference(reference)

    except Exception as e:
        logger.error(f"Error in query invoices reference api: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.delete('/reference/{reference}', summary='Delete invoice for reference', tags=[tags])
async def delete(reference: str, invoice_service: InvoiceService = Depends(get_service)):
    try:
        return invoice_service.delete(reference)

    except Exception as e:
        logger.error(f"Error in delte invoices reference api: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.post('/reference/{reference}/{email}', summary='Sendeer mail with invoice for reference', tags=[tags])
async def sender_email(reference: str, email: str, invoice_service: InvoiceService = Depends(get_service)):
    try:
        return invoice_service.sender_email(reference, email)

    except Exception as e:
        logger.error(f"Error in sender email with invoices reference api: {e}")
        raise HTTPException(status_code=400, detail=str(e))
