from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.mailer import Mailer
from app.core.security import get_current_user
from app.repositories.address_contract_repository import AndressContractRepository
from app.repositories.address_instructor_repository import AddressInstructorRepository
from app.repositories.contractor_repository import ContractorRepository
from app.repositories.execution_repository import ExecutionRepository
from app.repositories.instructor_payment_repository import InstructorPaymentRepository
from app.repositories.instructor_repository import InstructorRepository
from app.repositories.procedure_repository import ProcedureRepository
from app.repositories.procedure_schedule_repository import ProcedureScheduleRepository
from app.repositories.responsible_contract_repository import ResponsibleContractRepository
from app.repositories.schedule_repository import ScheduleRepository
from app.repositories.skill_repository import SkillRepository
from app.repositories.skill_schedule_repository import SkillScheduleRepository
from app.repositories.student_repository import StudentRepository
from app.repositories.user_repository import UserRepository
from app.schemas.execution_schemas import ExecutionSchemaIn, ExecutionSchemaOut
from app.services.address_contract_service import AddressContractService
from app.services.contractor_service import ContractorService
from app.services.execution_service import ExecutionService
from app.services.instructor_service import InstructorService
from app.services.procedure_schedule_service import ProcedureScheduleService
from app.services.procedure_service import ProcedureService
from app.services.responsible_contract_service import ResponsibleContractService
from app.services.schedule_service import ScheduleService
from app.services.skill_schedule_service import SkillScheduleService
from app.services.skill_service import SkillService
from app.services.student_service import StudentService
from app.services.user_service import UserService
from app.services.billing_service import BillingService
from app.repositories.billing_repository import BillingRepository
from app.services.payment_service import PaymentService
from app.repositories.payment_repository import PaymnentRepository
from db import get_db
from db.models import User
import logging

router = APIRouter()

tags: str = "Excecution"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_service(session: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    schedule_repository = ScheduleRepository(session, current_user)
    student_repository = StudentRepository(session, current_user)
    instructor_repository = InstructorRepository(session, current_user)
    skill_repository = SkillRepository(session, current_user)
    skill_schedule_repository = SkillScheduleRepository(session)
    execution_repository = ExecutionRepository(session, current_user)
    procedure_repository = ProcedureRepository(session)
    address_instructor_respository = AddressInstructorRepository(session)
    instructor_payment_repository = InstructorPaymentRepository(session)
    contractor_repository = ContractorRepository(session, current_user)
    responsible_contract_respository = ResponsibleContractRepository(
        session, current_user)
    address_contract_respository = AndressContractRepository(
        session, current_user)
    procedure_schedule_repository = ProcedureScheduleRepository(session)
    user_repository = UserRepository(session, current_user)
    billing_repository = BillingRepository(session, current_user)
    mailer = Mailer()

    address_contract_service = AddressContractService(
        address_contract_respository)
    contractor_service = ContractorService(contractor_repository)
    responsible_contract_service = ResponsibleContractService(
        responsible_contract_respository)
    address_instructor_repository = AddressInstructorRepository(
        address_instructor_respository)
    student_service = StudentService(
        student_repository,
        contractor_service,
        responsible_contract_service,
        address_contract_service)
    user_service = UserService(user_repository, mailer)
    instructor_service = InstructorService(
        instructor_repository, user_service, address_instructor_repository, instructor_payment_repository)
    procedure_service = ProcedureService(procedure_repository)
    skill_service = SkillService(skill_repository, procedure_service)
    skill_schedule_service = SkillScheduleService(skill_schedule_repository)
    procedure_schedule_service = ProcedureScheduleService(
        procedure_schedule_repository)
    billing_service = BillingService(billing_repository)
    payment_repository = PaymnentRepository(session, current_user)
    payment_service = PaymentService(payment_repository)

    schedule_service = ScheduleService(
        schedule_repository,
        student_service,
        instructor_service,
        skill_service,
        skill_schedule_service,
        execution_repository,
        procedure_service,
        procedure_schedule_service,
        payment_service,
        billing_service
    )

    return ExecutionService(execution_repository, schedule_service, procedure_schedule_service)


@router.post('/', summary='Create execution', response_model=ExecutionSchemaOut, tags=[tags])
async def create(execution_in: ExecutionSchemaIn, execution_service: ExecutionService = Depends(get_service)):
    try:
        execution = execution_service.create(execution_in)
        return ExecutionSchemaOut.from_orm(execution)

    except Exception as e:
        logger.error(f"Error in create execution: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.get('/{schedule_id}/{procedure_id}', summary='Return execution list for scheduled', response_model=List[ExecutionSchemaOut], tags=[tags])
async def get_shedule_procedure(schedule_id: UUID, procedure_id: UUID, execution_service: ExecutionService = Depends(get_service)):
    try:
        execution = execution_service.get_shedule_procedure(
            schedule_id, procedure_id)
        return [ExecutionSchemaOut.from_orm(x) for x in execution]

    except Exception as e:
        logger.error(f"Error in query execution list for scheduled: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.get('/{id}', summary='Return execution', response_model=ExecutionSchemaOut, tags=[tags])
async def get_id(id: UUID, execution_service: ExecutionService = Depends(get_service)):
    try:
        execution = execution_service.get_id(id)
        return ExecutionSchemaOut.from_orm(execution)

    except Exception as e:
        logger.error(f"Error in query execution: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.put('/{id}', summary='Update execution', response_model=ExecutionSchemaOut, tags=[tags])
async def update(id: UUID, execution_in: ExecutionSchemaIn, execution_service: ExecutionService = Depends(get_service)):
    try:
        execution = execution_service.update(id, execution_in)
        return ExecutionSchemaOut.from_orm(execution)

    except Exception as e:
        logger.error(f"Error in update execution: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.delete('/{id}', summary='Delete execution', tags=[tags])
async def update(id: UUID, execution_service: ExecutionService = Depends(get_service)):
    try:
        return execution_service.delete(id)

    except Exception as e:
        logger.error(f"Error in delete execution: {e}")
        raise HTTPException(status_code=400, detail=str(e))
