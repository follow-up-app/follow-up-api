import logging
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from app.repositories.avatar_repository import AvatarRepository
from app.services.avatar_service import AvatarService
from db import get_db
from sqlalchemy.orm import Session


router = APIRouter()

tags: str = "Avatars"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_service(session: Session = Depends(get_db)):
    avatar_repository = AvatarRepository(session)
    return AvatarService(avatar_repository)


@router.get('/student/{student_id}', summary='Return student avatar media', tags=[tags])
async def get_student(student_id: UUID, avatar_service: AvatarService = Depends(get_service)):
    try:
        img = avatar_service.get_path_student_avatar(student_id)
        if img:
            return FileResponse(img, media_type="image/jpeg")

    except Exception as e:
        logger.error(f"Error in load avatar: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.get('/user/{user_id}', summary='Return user avatar media', tags=[tags])
async def get_user(user_id: UUID, avatar_service: AvatarService = Depends(get_service)):
    try:
        img = avatar_service.get_path_user_avatar(user_id)
        if img:
            return FileResponse(img, media_type="image/jpeg")

    except Exception as e:
        logger.error(f"Error in load avatar: {e}")
        raise HTTPException(status_code=400, detail=str(e))
