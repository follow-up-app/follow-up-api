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
from app.repositories.payment_repository import PaymnentRepository
from app.repositories.procedure_repository import ProcedureRepository
from app.repositories.procedure_schedule_repository import ProcedureScheduleRepository
from app.repositories.responsible_contract_repository import ResponsibleContractReposioty
from app.repositories.schedule_repository import ScheduleRepository
from app.repositories.skill_repository import SkillRepository
from app.repositories.skill_schedule_repository import SkillScheduleRepository
from app.repositories.student_repository import StudentRepository
from app.repositories.user_repository import UserRepository
from app.services.address_contract_service import AddressContractService
from app.services.contractor_service import ContractorService
from app.services.execution_service import ExecutionService
from app.services.follow_up_service import FollowUpService
from app.services.instructor_service import InstructorService
from app.services.payment_service import PaymentService
from app.services.procedure_schedule_service import ProcedureScheduleService
from app.services.procedure_service import ProcedureService
from app.services.queue_service import QueueService
from app.services.responsible_contract_service import ResponsibleContractService
from app.services.schedule_service import ScheduleService
from app.services.skill_schedule_service import SkillScheduleService
from app.services.skill_service import SkillService
from app.services.student_service import StudentService
from app.services.user_service import UserService
from db import get_db
from db.models import User
from app.schemas.schedule_schemas import ScheduleSchemaOut
from app.schemas.follow_up_schemas import FiltersSchemaIn, ScheduleSchemaFollowUp, ScheduleSchemaFollowUpMobile
import logging


router = APIRouter()

tags: str = "Follow-up"

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
    responsible_contract_respository = ResponsibleContractReposioty(
        session, current_user)
    address_contract_respository = AndressContractRepository(
        session, current_user)
    procedure_schedule_repository = ProcedureScheduleRepository(session)
    user_repository = UserRepository(session, current_user)
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
        payment_service
    )

    execution_service = ExecutionService(
        execution_repository, schedule_service, procedure_schedule_service)

    return FollowUpService(schedule_service, skill_schedule_service, skill_service, procedure_schedule_service, execution_service)


@router.get('/', summary='Return follow-up list', response_model=List[ScheduleSchemaOut], tags=[tags])
async def get_follow_up(follow_up_service: FollowUpService = Depends(get_service)):
    try:
        follow_ups = follow_up_service.get_follow_up()
        return [ScheduleSchemaOut.from_orm(x) for x in follow_ups]

    except Exception as e:
        logger.error(f"Error in query follow-up: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.get('/schedule/{schedule_id}', summary='Return result detail', response_model=ScheduleSchemaFollowUp, tags=[tags])
async def get_follow_up_schedule(schedule_id: UUID, follow_up_service: FollowUpService = Depends(get_service)):
    try:
        follow_up = follow_up_service.get_follow_up_schedule(schedule_id)
        return ScheduleSchemaFollowUp.from_orm(follow_up)

    except Exception as e:
        logger.error(f"Error in query follow-up schedule id: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.get('/mobile-schedule/{schedule_id}/{skill_schedule_id}', summary='Return result detail', response_model=ScheduleSchemaFollowUpMobile, tags=[tags])
async def mobile_schedule(schedule_id: UUID, skill_schedule_id: UUID, follow_up_service: FollowUpService = Depends(get_service)):
    try:
        follow_up = follow_up_service.mobile_schedule(
            schedule_id, skill_schedule_id)
        return ScheduleSchemaFollowUpMobile.from_orm(follow_up)

    except Exception as e:
        logger.error(f"Error in query follow-up mobile schedule: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.post('/filters/', summary='Return filter result followups', response_model=List[ScheduleSchemaOut], tags=[tags])
async def get_filters(filters_in: FiltersSchemaIn, follow_up_service: FollowUpService = Depends(get_service)):
    try:
        follow_ups = follow_up_service.get_filters(filters_in)
        return [ScheduleSchemaOut.from_orm(x) for x in follow_ups]

    except Exception as e:
        logger.error(f"Error in query follow-up mobile schedule: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.get('/student/{student_id}', summary='Return result details', response_model=ScheduleSchemaOut, tags=[tags])
async def get_id(student_id: UUID,  follow_up_service: FollowUpService = Depends(get_service)):
    try:
        follow_up = follow_up_service.get_student(student_id)
        return ScheduleSchemaOut.from_orm(follow_up)

    except Exception as e:
        logger.error(f"Error in query follow-up mobile schedule: {e}")
        raise HTTPException(status_code=400, detail=str(e))
