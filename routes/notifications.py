from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from core.security import get_current_user
from db import get_db
from db.models import User
from db.mongo import Mongo
from bson import json_util
import json


router = APIRouter()

tag: str = "Notifications"


@router.get('/', summary='Returns notifications list')
async def get_all(current_user: User = Depends(get_current_user), session: Session = Depends(get_db)):
    mongo = Mongo()
    response = mongo.get_notifications(current_user.id)
    return json.loads(json_util.dumps(response))
     

@router.get('/read', summary='Returns users list')
async def get_all(current_user: User = Depends(get_current_user), session: Session = Depends(get_db)):
    pass