from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.security import get_current_user, hash_password
from db import get_db
from db.models import User
from schemas.user_schemas import RecoveryPasswordSchemaIn, UserOut, ResetPasswordSchemaIn
import logging
from core.mailer import Mailer
from core.crypt import Crypt

router = APIRouter()

tags: str = "Profile"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@router.post('/recovery-password', summary='sender link password',  tags=[tags])
async def update(user_schema: RecoveryPasswordSchemaIn, session: Session = Depends(get_db)):
    user: User = User.query(session).filter(
        User.email == user_schema.email).first()
    if not user:
        raise HTTPException(status_code=404, detail='E-mail não cadastrado')

    try:
        mailer = Mailer()
        mailer.recovery_password(user)

        return UserOut.from_orm(user)
    
    except Exception as e:
        logger.error(f"Error in sender recovery email: {e}")
        raise HTTPException(status_code=500, detail='Server error')
    
    
@router.post('/refresh-password', summary='password',  tags=[tags])
async def update(user_schema: ResetPasswordSchemaIn, session: Session = Depends(get_db)):
    decrypt = Crypt.decrypt(user_schema.token)
    user: User = User.query(session).filter(User.id == decrypt[1]).first()
    if not user:
        raise HTTPException(status_code=404, detail='user not found')
       
    user.password_hash = hash_password(user_schema.password)
    
    try:    
        session.add(user)
        session.commit()
        
        return UserOut.from_orm(user)
    
    except Exception as e:
        logger.error(f"Error in refresh user password: {e}")
        raise HTTPException(status_code=500, detail='Server error')
    
    
@router.put('/update-password', summary='Update password', response_model=UserOut, tags=[tags])
async def update(user_schema: ResetPasswordSchemaIn, current_user: User = Depends(get_current_user), session: Session = Depends(get_db)):
    user: User = User.query(session).filter(User.id == current_user.id).first()
    if not user:
        raise HTTPException(status_code=404, detail='user not found')

    user.password_hash = hash_password(user_schema.password)
    
    try:    
        session.add(user)
        session.commit()
        
        return UserOut.from_orm(user)
    
    except Exception as e:
        logger.error(f"Error in password update user: {e}")
        raise HTTPException(status_code=500, detail='Server error')