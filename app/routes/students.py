from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, File
from sqlalchemy.orm import Session
from app.core.security import get_current_user
from app.repositories.address_contract_repository import AndressContractRepository
from app.repositories.contractor_repository import ContractorRepository
from app.repositories.responsible_contract_repository import ResponsibleContractReposioty
from app.repositories.student_repository import StudentRepository
from app.schemas.address_contract_schemas import AddressContractorSchemaIn, AddressContractorSchemaOut
from app.schemas.responsible_contract_schemas import ResponsibleContractSchemaIn, ResponsibleContractSchemaOut
from app.services.address_contract_service import AddressContractService
from app.services.contractor_service import ContractorService
from app.services.responsible_contract_service import ResponsibleContractService
from app.services.student_service import StudentService
from db import get_db
from db.models import User
from app.schemas.student_schemas import StudentSchemaIn, StudentSchemaOut, Filters
from fastapi.responses import FileResponse
import logging

router = APIRouter()

tags: str = "Student"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_service(session: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    student_repository = StudentRepository(session, current_user)
    contractor_repository = ContractorRepository(session, current_user)
    responsible_contract_respository = ResponsibleContractReposioty(
        session, current_user)
    address_contract_respository = AndressContractRepository(
        session, current_user)

    contractor_service = ContractorService(contractor_repository)
    responsible_contract_service = ResponsibleContractService(
        responsible_contract_respository)
    address_contract_service = AddressContractService(
        address_contract_respository)

    return StudentService(student_repository, contractor_service, responsible_contract_service, address_contract_service)


@router.post('/', summary='create student', response_model=StudentSchemaOut, tags=[tags])
async def create(student_in: StudentSchemaIn, student_service: StudentService = Depends(get_service)):
    try:
        student = student_service.create(student_in)
        return StudentSchemaOut.from_orm(student)

    except Exception as e:
        logger.error(f"Error in create student: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.get('/', summary='Returns students list', response_model=List[StudentSchemaOut], tags=[tags])
async def get_all(student_service: StudentService = Depends(get_service)):
    try:
        students = student_service.get_all()
        return [StudentSchemaOut.from_orm(x) for x in students]

    except Exception as e:
        logger.error(f"Error in query students: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    
    
@router.get('/actives/', summary='Returns students actives list', response_model=List[StudentSchemaOut], tags=[tags])
async def get_all_actives(student_service: StudentService = Depends(get_service)):
    try:
        students = student_service.get_all_actives()
        return [StudentSchemaOut.from_orm(x) for x in students]

    except Exception as e:
        logger.error(f"Error in query students actives: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.get('/{id}', summary='Returns student for id', response_model=StudentSchemaOut, tags=[tags])
async def get_id(id: UUID, student_service: StudentService = Depends(get_service)):
    try:
        student = student_service.get_id(id)
        return StudentSchemaOut.from_orm(student)

    except Exception as e:
        logger.error(f"Error in query student for id: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.get('/active/{id}/', summary='Update student status', response_model=StudentSchemaOut, tags=[tags])
async def update_active(id: UUID, student_service: StudentService = Depends(get_service)):
    try:
        student = student_service.update_active(id)
        return StudentSchemaOut.from_orm(student)

    except Exception as e:
        logger.error(f"Error in update student: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    
    
@router.patch('/{id}', summary='Update student', response_model=StudentSchemaOut, tags=[tags])
async def update(id: UUID, student_in: StudentSchemaIn, student_service: StudentService = Depends(get_service)):
    try:
        student = student_service.update(id, student_in)
        return StudentSchemaOut.from_orm(student)

    except Exception as e:
        logger.error(f"Error in update student: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.post('/{id}/avatar', summary='Upload avatar', tags=[tags])
async def create_avatar(id: UUID, file: bytes = File(...), student_service: StudentService = Depends(get_service)):
    try:
        student = student_service.save_avatar(id, file)
        return StudentSchemaOut.from_orm(student)

    except Exception as e:
        logger.error(f"Error in upload image in student: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.post('/{id}/responsible', summary='create responsible', response_model=ResponsibleContractSchemaOut, tags=[tags])
async def responsible_create(id: UUID, responsible_in: ResponsibleContractSchemaIn, student_service: StudentService = Depends(get_service)):
    try:
        responsible = student_service.create_responsible(id, responsible_in)
        return ResponsibleContractSchemaOut(responsible)

    except Exception as e:
        logger.error(f"Error in create responsible: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.get('/{id}/responsible', summary='Returns all responsible list', response_model=List[ResponsibleContractSchemaOut], tags=[tags])
async def responsible_get_all(id: UUID, student_service: StudentService = Depends(get_service)):
    try:
        responsibles = student_service.get_responsible_contractor(id)
        return [ResponsibleContractSchemaOut.from_orm(x) for x in responsibles]

    except Exception as e:
        logger.error(f"Error in list responsible: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.get('/responsible/{responsible_id}', summary='Return responsible', response_model=ResponsibleContractSchemaOut, tags=[tags])
async def responsible_get_id(responsible_id: UUID, student_service: StudentService = Depends(get_service)):
    try:
        responsible = student_service.get_responsible_id(responsible_id)
        return ResponsibleContractSchemaOut(responsible)

    except Exception as e:
        logger.error(f"Error in query responsible: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.patch('/responsible/{responsible_id}', summary='Update responsible', response_model=ResponsibleContractSchemaOut, tags=[tags])
async def responsible_update(responsible_id: UUID, responsible_in: ResponsibleContractSchemaIn, student_service: StudentService = Depends(get_service)):
    try:
        responsible = student_service.update_responsible(
            responsible_id, responsible_in)
        return ResponsibleContractSchemaOut(responsible)

    except Exception as e:
        logger.error(f"Error in query responsible: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.delete('/responsible/{responsible_id}', summary='Delete responsible', tags=[tags])
async def responsible_delete(responsible_id: UUID, student_service: StudentService = Depends(get_service)):
    try:
        return student_service.remove_responsible(responsible_id)

    except Exception as e:
        logger.error(f"Error in query responsible: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.post('/{id}/address', summary='create address', response_model=AddressContractorSchemaOut, tags=[tags])
async def responsible_create(id: UUID, address_in: AddressContractorSchemaIn, student_service: StudentService = Depends(get_service)):
    try:
        address = student_service.create_address(id, address_in)
        return AddressContractorSchemaOut.from_orm(address)

    except Exception as e:
        logger.error(f"Error in create address contract: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.get('/{id}/address', summary='Return contract address', response_model=AddressContractorSchemaOut, tags=[tags])
async def address_get_id(id: UUID, student_service: StudentService = Depends(get_service)):
    try:
        address = student_service.get_address_contractor(id)
        return AddressContractorSchemaOut.from_orm(address)

    except Exception as e:
        logger.error(f"Error in list address: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.patch('/address/{address_id}', summary='Update contract address', response_model=AddressContractorSchemaOut, tags=[tags])
async def address_update(address_id: UUID, address_in: AddressContractorSchemaIn, student_service: StudentService = Depends(get_service)):
    try:
        address = student_service.update_address(address_id, address_in)
        return AddressContractorSchemaOut.from_orm(address)

    except Exception as e:
        logger.error(f"Error in update address: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.post('/filters', summary='Return list with filters',  response_model=List[StudentSchemaOut], tags=[tags])
async def get_filters(filters_in: Filters, student_service: StudentService = Depends(get_service)):
    try:
        students = student_service.filters(filters_in)
        return [StudentSchemaOut.from_orm(x) for x in students]

    except Exception as e:
        logger.error(f"Error in filter students: {e}")
        raise HTTPException(status_code=400, detail=str(e))
