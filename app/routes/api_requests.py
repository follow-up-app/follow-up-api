from fastapi import APIRouter, Depends, HTTPException
from app.core.api_requests import ApiRequests
from app.services.api_requests_service import ApiRequestsService
import logging


router = APIRouter()

tags: str = "Api-requests"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_service():
    return ApiRequestsService()


@router.get('/banks', summary='Returns banfks of list', tags=[tags])
async def banks(api_requests_service: ApiRequestsService = Depends(get_service)):
    try:
        return api_requests_service.banks()

    except Exception as e:
        logger.error(f"Error in query skills: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.get('/cep/{cep}', summary='Returns banfks of list', tags=[tags])
async def banks(cep: str, api_requests_service: ApiRequestsService = Depends(get_service)):
    try:
        return api_requests_service.cep(cep)

    except Exception as e:
        logger.error(f"Error in query skills: {e}")
        raise HTTPException(status_code=400, detail=str(e))
