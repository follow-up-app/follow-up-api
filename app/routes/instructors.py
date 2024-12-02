from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, File
from sqlalchemy.orm import Session
from app.core.security import get_current_user
from app.repositories.address_instructor_repository import AddressInstructorRepository
from app.repositories.instructor_payment_repository import InstructorPaymentRepository
from app.repositories.instructor_repository import InstructorRepository
from app.repositories.user_repository import UserRepository
from app.schemas.address_instructor_schemas import AddressInstructorSchemaIn, AddressInstructorSchemaOut
from app.schemas.instructor_payment_schema import InstructorPaymentSchemaIn, InstructorPaymentSchemaOut
from app.schemas.user_schemas import UserSchemaOut
from app.services.instructor_service import InstructorService
from app.services.user_service import UserService
from db import get_db
from db.models import User
from app.schemas.instructor_schema import InstructorSchemaOut, InstructorSchemaIn, Filters
from fastapi.responses import FileResponse
from app.core.mailer import Mailer
import logging


router = APIRouter()

tags: str = "Instructors"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_service(session: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    instructor_repository = InstructorRepository(session, current_user)
    user_repository = UserRepository(session, current_user)
    mailer = Mailer()
    user_service = UserService(user_repository, mailer)

    address_instructor_respository = AddressInstructorRepository(session)
    instructor_payment_respository = InstructorPaymentRepository(session)
    return InstructorService(instructor_repository, user_service, address_instructor_respository, instructor_payment_respository)


@router.post('/', summary='create instructor', response_model=InstructorSchemaOut, tags=[tags])
async def create(instructor_in: InstructorSchemaIn, instructor_service: InstructorService = Depends(get_service)):
    try:
        instructor = instructor_service.create(instructor_in)
        return InstructorSchemaOut.from_orm(instructor)

    except Exception as e:
        logger.error(f"Error in create instructor: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.get('/', summary='Returns instructors list', response_model=List[InstructorSchemaOut], tags=[tags])
async def get_all(instructor_service: InstructorService = Depends(get_service)):
    try:
        instructors = instructor_service.get_all()
        return [InstructorSchemaOut.from_orm(x) for x in instructors]

    except Exception as e:
        logger.error(f"Error in query instructors: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.get('/{id}', summary='Returns student for id', response_model=InstructorSchemaOut, tags=[tags])
async def get_id(id: UUID, instructor_service: InstructorService = Depends(get_service)):
    try:
        instructor = instructor_service.get_id(id)
        return InstructorSchemaOut.from_orm(instructor)

    except Exception as e:
        logger.error(f"Error in query instructor for id: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.patch('/{id}', summary='Update student', response_model=InstructorSchemaOut, tags=[tags])
async def update(id: UUID, instructor_in: InstructorSchemaIn, instructor_service: InstructorService = Depends(get_service)):
    try:
        instructor = instructor_service.update(id, instructor_in)
        return InstructorSchemaOut.from_orm(instructor)

    except Exception as e:
        logger.error(f"Error in update instructor: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.post('/{id}/avatar', summary='Upload avatar', response_model=UserSchemaOut, tags=[tags])
async def create_avatar(id: UUID, file: bytes = File(...), instructor_service: InstructorService = Depends(get_service)):
    try:
        user = instructor_service.save_avatar(id, file)
        return UserSchemaOut.from_orm(user)

    except Exception as e:
        logger.error(f"Error in upload image in instructor: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.get('/{id}/avatar', summary='Return avatar instructor', tags=[tags])
async def get_avatar(id: UUID, instructor_service: InstructorService = Depends(get_service)):
    try:
        img = instructor_service.avatar(id)
        return FileResponse(img, media_type="image/jpeg")

    except Exception as e:
        logger.error(f"Error in upload image in instructor: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.post('/{id}/address', summary='Create instructor address', response_model=AddressInstructorSchemaOut, tags=[tags])
async def address_create(id: UUID, address_in: AddressInstructorSchemaIn, instructor_service: InstructorService = Depends(get_service)):
    try:
        address = instructor_service.create_address(id, address_in)
        return AddressInstructorSchemaOut.from_orm(address)

    except Exception as e:
        logger.error(f"Error in create address instructor: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.get('/{id}/address', summary='Return instructor address', response_model=AddressInstructorSchemaOut, tags=[tags])
async def address_get_id(id: UUID, instructor_service: InstructorService = Depends(get_service)):
    try:
        address = instructor_service.get_address(id)
        return AddressInstructorSchemaOut.from_orm(address)

    except Exception as e:
        logger.error(f"Error in list address: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.patch('/address/{address_id}', summary='Update instructor address', response_model=AddressInstructorSchemaOut, tags=[tags])
async def address_update(address_id: UUID, address_in: AddressInstructorSchemaIn, instructor_service: InstructorService = Depends(get_service)):
    try:
        address = instructor_service.update_address(address_id, address_in)
        return AddressInstructorSchemaOut.from_orm(address)

    except Exception as e:
        logger.error(f"Error in update address: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.get('/actives/', summary='Returns instructors actives list', response_model=List[InstructorSchemaOut], tags=[tags])
async def get_actives_all(instructor_service: InstructorService = Depends(get_service)):
    try:
        instructors = instructor_service.get_actives_all()
        return [InstructorSchemaOut.from_orm(x) for x in instructors]

    except Exception as e:
        logger.error(f"Error in query instructors: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.get('/active/{id}/', summary='Active or inctive instructor in app', response_model=InstructorSchemaOut, tags=[tags])
async def update_active(id: UUID, instructor_service: InstructorService = Depends(get_service)):
    try:
        instructor = instructor_service.update_active(id)
        return InstructorSchemaOut.from_orm(instructor)

    except Exception as e:
        logger.error(f"Error in active instructor: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.post('/filters', summary='Return list with filters',  response_model=List[InstructorSchemaOut], tags=[tags])
async def get_filters(filters_in: Filters, instructor_service: InstructorService = Depends(get_service)):
    try:
        instructors = instructor_service.get_filters(filters_in)
        return [InstructorSchemaOut.from_orm(x) for x in instructors]

    except Exception as e:
        logger.error(f"Error in filter instructors: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.post('/{id}/data-payment', summary='Create details for payment',  response_model=InstructorSchemaOut, tags=[tags])
async def create_payment(id: UUID, instructor_payment_in: InstructorPaymentSchemaIn, instructor_service: InstructorService = Depends(get_service)):
    try:
        instructor = instructor_service.create_data_payment(
            id, instructor_payment_in)
        return InstructorSchemaOut.from_orm(instructor)

    except Exception as e:
        logger.error(f"Error in create instructor data payment: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.patch('/{id}/data-payment', summary='Update instructor details for payment',  response_model=InstructorSchemaOut, tags=[tags])
async def update_bank_payment(id: UUID, instructor_payment_in: InstructorPaymentSchemaIn, instructor_service: InstructorService = Depends(get_service)):
    try:
        instructor = instructor_service.update_data_payment(
            id, instructor_payment_in)
        return InstructorSchemaOut.from_orm(instructor)

    except Exception as e:
        logger.error(f"Error in update instructor bank payment: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.get('/{id}/data-payment', summary='return instructor details for payment',  response_model=InstructorPaymentSchemaOut, tags=[tags])
async def get_bank_payment(id: UUID, instructor_service: InstructorService = Depends(get_service)):
    try:
        instructor = instructor_service.get_data_payment(id)
        return InstructorPaymentSchemaOut.from_orm(instructor)

    except Exception as e:
        logger.error(f"Error in query instructor bank payment: {e}")
        raise HTTPException(status_code=400, detail=str(e))
