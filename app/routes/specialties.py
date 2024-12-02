from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import logging
from app.core.security import get_current_user
from app.repositories.specialty_repository import SpecialtyRepository
from app.schemas.specialty_schemas import SpecialtySchemaIn, SpecialtySchemaOut
from app.services.specialty_service import SpecialtyService
from db import get_db
from db.models import User

router = APIRouter()

tags: str = "Specialty"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_service(session: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    specialty_repository = SpecialtyRepository(session, current_user)

    return SpecialtyService(specialty_repository)


@router.post('/', summary='Create specialty', response_model=SpecialtySchemaOut, tags=[tags])
async def create(specialty_in: SpecialtySchemaIn, specialty_service: SpecialtyService = Depends(get_service)):
    try:
        specialty = specialty_service.create(specialty_in)
        return SpecialtySchemaOut.from_orm(specialty)

    except Exception as e:
        logger.error(f"Error in create specialty: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.get('/', summary='Return all specialties', response_model=List[SpecialtySchemaOut], tags=[tags])
async def get_all(specialty_service: SpecialtyService = Depends(get_service)):
    try:
        specialties = specialty_service.get_all()
        return [SpecialtySchemaOut.from_orm(x) for x in specialties]

    except Exception as e:
        logger.error(f"Error in query specialties: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.get('/{id}', summary='Return specialty', response_model=SpecialtySchemaOut, tags=[tags])
async def get_id(id: UUID, specialty_service: SpecialtyService = Depends(get_service)):
    try:
        specialty = specialty_service.get_id(id)
        return SpecialtySchemaOut.from_orm(specialty)

    except Exception as e:
        logger.error(f"Error in query specialty: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.patch('/{id}', summary='Update specialty', response_model=SpecialtySchemaOut, tags=[tags])
async def update(id: UUID, specialty_in: SpecialtySchemaIn, specialty_service: SpecialtyService = Depends(get_service)):
    try:
        specialty = specialty_service.update(id, specialty_in)
        return SpecialtySchemaOut.from_orm(specialty)

    except Exception as e:
        logger.error(f"Error in update specialty: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.delete('/{id}', summary='Delete specialty', tags=[tags])
async def delete(id: UUID, specialty_service: SpecialtyService = Depends(get_service)):
    try:
        return specialty_service.delete(id)

    except Exception as e:
        logger.error(f"Error in delete specialty: {e}")
        raise HTTPException(status_code=400, detail=str(e))
