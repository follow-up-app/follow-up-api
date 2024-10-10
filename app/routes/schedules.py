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
from app.schemas.procedure_schemas import ProcedureSchemaIn, ProcedureSchemaOut
from app.services.address_contract_service import AddressContractService
from app.services.contractor_service import ContractorService
from app.services.instructor_service import InstructorService
from app.services.payment_service import PaymentService
from app.services.procedure_schedule_service import ProcedureScheduleService
from app.services.procedure_service import ProcedureService
from app.services.responsible_contract_service import ResponsibleContractService
from app.services.schedule_service import ScheduleService
from app.services.skill_schedule_service import SkillScheduleService
from app.services.skill_service import SkillService
from app.services.student_service import StudentService
from app.services.user_service import UserService
from app.repositories.billing_repository import BillingRepository
from app.services.billing_service import BillingService
from db import get_db
from db.models import User
from app.schemas.schedule_schemas import ProcedureScheduleSchemaIn, ScheduleSchemaIn, ScheduleSchemaOut, ScheduleUpadateSchamaIn
import logging


router = APIRouter()

tags: str = "Schedule"

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
    billing_repository = BillingRepository(session, current_user)
    mailer = Mailer()

    address_contract_service = AddressContractService(
        address_contract_respository)
    contractor_service = ContractorService(contractor_repository)
    responsible_contract_service = ResponsibleContractService(
        responsible_contract_respository)
    address_instructor_respository = AddressInstructorRepository(
        address_instructor_respository)
    student_service = StudentService(
        student_repository,
        contractor_service,
        responsible_contract_service,
        address_contract_service)
    user_service = UserService(user_repository, mailer)
    instructor_service = InstructorService(
        instructor_repository, user_service, address_instructor_respository, instructor_payment_repository)
    procedure_service = ProcedureService(procedure_repository)
    skill_service = SkillService(skill_repository, procedure_service)
    skill_schedule_service = SkillScheduleService(skill_schedule_repository)
    procedure_schedule_service = ProcedureScheduleService(
        procedure_schedule_repository)
    payment_repository = PaymnentRepository(session, current_user)
    payment_service = PaymentService(payment_repository)
    billing_service = BillingService(billing_repository)

    return ScheduleService(
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


@router.post('/', summary='Create schedule', response_model=List[ScheduleSchemaOut], tags=[tags])
async def create(schedule_in: ScheduleSchemaIn, schedule_service: ScheduleService = Depends(get_service)):
    try:
        schedules = schedule_service.create(schedule_in)
        return [ScheduleSchemaOut.from_orm(x) for x in schedules]

    except Exception as e:
        logger.error(f"Error in create schedule: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.get('/', summary='Return schedule list', response_model=List[ScheduleSchemaOut], tags=[tags])
async def get_all(schedule_service: ScheduleService = Depends(get_service)):
    try:
        schedules = schedule_service.get_all()
        return [ScheduleSchemaOut.from_orm(x) for x in schedules]

    except Exception as e:
        logger.error(f"Error in query schedule: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.get('/details/{id}', summary='Return schedule', tags=[tags])
async def get_id(id: UUID, schedule_service: ScheduleService = Depends(get_service)):
    try:
        schedule = schedule_service.get_id(id)
        return ScheduleSchemaOut.from_orm(schedule)

    except Exception as e:
        logger.error(f"Error in query schedule for id: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.get('/scheduled', summary='Return schedule list for scheduled status', response_model=List[ScheduleSchemaOut], tags=[tags])
async def get_scheduled(schedule_service: ScheduleService = Depends(get_service)):
    try:
        schedules = schedule_service.get_schedule()
        return [ScheduleSchemaOut.from_orm(x) for x in schedules]

    except Exception as e:
        logger.error(f"Error in query schedule: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.get('list/{instructor_id}', summary='Return schedule list for instructor', response_model=List[ScheduleSchemaOut], tags=[tags])
async def get_all(instructor_id: UUID, schedule_service: ScheduleService = Depends(get_service)):
    try:
        schedules = schedule_service.get_instructor(instructor_id)
        return [ScheduleSchemaOut.from_orm(x) for x in schedules]

    except Exception as e:
        logger.error(f"Error in query instructor schedule: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.delete('/events/{event_id}', summary='Remove all schedules', tags=[tags])
async def delete_many(event_id: UUID, schedule_service: ScheduleService = Depends(get_service)):
    try:
        return schedule_service.delete_many(event_id)

    except Exception as e:
        logger.error(f"Error in delete many schedules: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.delete('/{id}', summary='Delete schedule', tags=[tags])
async def delete_unique(id: UUID, schedule_service: ScheduleService = Depends(get_service)):
    try:
        return schedule_service.delete(id)

    except Exception as e:
        logger.error(f"Error in delete unique schedule: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.put('/{id}/update', summary='Update status schedule', response_model=ScheduleSchemaOut, tags=[tags])
async def update(id: UUID, schedule_in: ScheduleUpadateSchamaIn, schedule_service: ScheduleService = Depends(get_service)):
    try:
        schedule = schedule_service.update(id, schedule_in)
        return ScheduleSchemaOut.from_orm(schedule)

    except Exception as e:
        logger.error(f"Error in update schedule: {e}")
        raise HTTPException(status_code=500, detail='Server error')


@router.get('/schedule-today', summary='Return all schedule today', response_model=List[ScheduleSchemaOut], tags=[tags])
async def get_today(schedule_service: ScheduleService = Depends(get_service)):
    try:
        schedules = schedule_service.get_today()
        return [ScheduleSchemaOut.from_orm(x) for x in schedules]

    except Exception as e:
        logger.error(f"Error in query schedule today: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.get('/avalible-instructor', summary='Return schedule list mobile', tags=[tags])
async def get_avalible_instructor(schedule_service: ScheduleService = Depends(get_service)):
    try:
        return schedule_service.get_avalible_instructor()

    except Exception as e:
        logger.error(f"Error in query schedule mobile: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.get('/{id}/student-arrival', summary='Student arrival', response_model=ScheduleSchemaOut, tags=[tags])
async def get_id(id: UUID, schedule_service: ScheduleService = Depends(get_service)):
    try:
        schedule = schedule_service.student_arrival(id)
        return ScheduleSchemaOut.from_orm(schedule)

    except Exception as e:
        logger.error(f"Error in student arrival: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.get('/{id}/{skill_id}/procedures/', summary='Return all schedule today', response_model=List[ProcedureSchemaOut], tags=[tags])
async def get_produre(id: UUID, skill_id: UUID, schedule_service: ScheduleService = Depends(get_service)):
    try:
        procedures = schedule_service.get_procedures(id, skill_id)
        return [ProcedureSchemaOut.from_orm(x) for x in procedures]

    except Exception as e:
        logger.error(f"Error in query procedure schedule: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.patch('/procedure/{procedure_schedule_id}', summary='Update procedure schedule', response_model=ProcedureSchemaOut, tags=[tags])
async def update_procedure_schedule(procedure_schedule_id: UUID, procedure_in: ProcedureSchemaIn, schedule_service: ScheduleService = Depends(get_service)):
    try:
        procedure_schedule = schedule_service.update_procedure_schedule(
            procedure_schedule_id, procedure_in)
        return ProcedureSchemaOut.from_orm(procedure_schedule)

    except Exception as e:
        logger.error(f"Error in update procedure schedule: {e}")
        raise HTTPException(status_code=500, detail='Server error')


@router.post('/{id}/procedures/', summary='add procedure in schedule', response_model=List[ScheduleSchemaOut], tags=[tags])
async def add_procedure(id: UUID, procedure_in: ProcedureScheduleSchemaIn, schedule_service: ScheduleService = Depends(get_service)):
    try:
        schedules = schedule_service.add_procedure_schedule(
            id, procedure_in.procedure_id)
        return [ScheduleSchemaOut.from_orm(x) for x in schedules]

    except Exception as e:
        logger.error(f"Error in add procedure in schedule: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.delete('/procedures/{procedure_schedule_id}', summary='Delete procedure schedule', tags=[tags])
async def delete_procedure(procedure_schedule_id: UUID, schedule_service: ScheduleService = Depends(get_service)):
    try:
        return schedule_service.delete_procedure_schedule(procedure_schedule_id)

    except Exception as e:
        logger.error(f"Error in delete procedure in schedule: {e}")
        raise HTTPException(status_code=400, detail=str(e))
