from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db import get_db
from app.core.security import get_current_user
from app.schemas.health_plan_schemas import HealthPlanSchemaIn, HealthPlanSchemaOut
import logging
from app.services.health_plan_service import HealthPlanService
from app.repositories.health_plan_repository import HealthPlanRepository
from db.models import User


router = APIRouter()

tags: str = "Health Plans"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_service(session: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    health_plan_repository = HealthPlanRepository(session, current_user)
    return HealthPlanService(health_plan_repository)


@router.post('/', summary='Create health plan', response_model=HealthPlanSchemaOut, tags=[tags])
async def create(plan_in: HealthPlanSchemaIn, plan_service: HealthPlanService = Depends(get_service)):
    try:
        plan = plan_service.create(plan_in)
        return HealthPlanSchemaOut.from_orm(plan)

    except Exception as e:
        logger.error(f"Error in create health plan: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.get('/', summary='Return health plan list', response_model=List[HealthPlanSchemaOut], tags=[tags])
async def get_all(plan_service: HealthPlanService = Depends(get_service)):
    try:
        plans = plan_service.get_all()
        return [HealthPlanSchemaOut.from_orm(x) for x in plans]

    except Exception as e:
        logger.error(f"Error in query health plans: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.get('/{id}', summary='Return health plans for id', response_model=HealthPlanSchemaOut, tags=[tags])
async def get_id(id: UUID, plan_service: HealthPlanService = Depends(get_service)):
    try:
        plan = plan_service.get_id(id)
        return HealthPlanSchemaOut.from_orm(plan)

    except Exception as e:
        logger.error(f"Error in query  health plan for id: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.patch('/{id}', summary='Update  health plan', response_model=HealthPlanSchemaOut, tags=[tags])
async def update(id: UUID, plan_in: HealthPlanSchemaIn, plan_service: HealthPlanService = Depends(get_service)):
    try:
        plan = plan_service.update(id, plan_in)
        return HealthPlanSchemaOut.from_orm(plan)

    except Exception as e:
        logger.error(f"Error in update  health plan: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.delete('/{de}', summary='delete health plan', tags=[tags])
async def delete(id: UUID, plan_service: HealthPlanService = Depends(get_service)):
    try:
        plan = plan_service.remove(id)
        return HealthPlanSchemaOut.from_orm(plan)

    except Exception as e:
        logger.error(f"Error in update  health plan: {e}")
        raise HTTPException(status_code=400, detail=str(e))
