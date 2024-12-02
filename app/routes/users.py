from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, File
from sqlalchemy.orm import Session
from app.core.security import get_current_user
from db import get_db
from app.schemas.user_schemas import UserSchemaOut, UserSchemaIn
from fastapi.responses import FileResponse
from app.core.mailer import Mailer
from app.repositories.user_repository import UserRepository
from app.services.user_service import UserService
from db.models import User
import logging



router = APIRouter()

tags: str = "Users"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_service(session: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    user_repository = UserRepository(session, current_user)
    mailer = Mailer()
    return UserService(user_repository, mailer)


@router.post('/', summary='Create user', response_model=UserSchemaOut, tags=[tags])
async def create(user_in: UserSchemaIn, user_service: UserService = Depends(get_service)):
    try:
        user = user_service.create(user_in)
        return UserSchemaOut.from_orm(user)

    except Exception as e:
        logger.error(f"Error in create user: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.get('/', summary='Returns users list', response_model=List[UserSchemaOut], tags=[tags])
async def get_all(user_service: UserService = Depends(get_service)):
    try:
        users = user_service.get_all()
        return [UserSchemaOut.from_orm(x) for x in users]

    except Exception as e:
        logger.error(f"Error in query users: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.get('/{id}', summary='Returns user for id', response_model=List[UserSchemaOut], tags=[tags])
async def get_id(id: UUID, user_service: UserService = Depends(get_service)):
    try:
        user = user_service.get_id(id)
        return [UserSchemaOut.from_orm(user)]

    except Exception as e:
        logger.error(f"Error in query company for id: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.patch('/{id}', summary='Update user', response_model=UserSchemaOut, tags=[tags])
async def update(id: UUID, user_in: UserSchemaIn, user_service: UserService = Depends(get_service)):
    try:
        user = user_service.update(id, user_in)
        return UserSchemaOut.from_orm(user)

    except Exception as e:
        logger.error(f"Error in update user: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.post('/{id}/avatar', summary='Upload avatar', response_model=UserSchemaOut, tags=[tags])
async def create(id: UUID, file: bytes = File(...), user_service: UserService = Depends(get_service)):
    try:
        user = user_service.save_avatar(id, file)
        return UserSchemaOut.from_orm(user)

    except Exception as e:
        logger.error(f"Error in upload image in user: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.get('/{id}/avatar', summary='Return avatar user', tags=[tags])
async def get_id(id: UUID, user_service: UserService = Depends(get_service)):
    try:
        img = user_service.avatar(id)
        return FileResponse(img, media_type="image/jpeg")

    except Exception as e:
        logger.error(f"Error in upload image in user: {e}")
        raise HTTPException(status_code=400, detail=str(e))