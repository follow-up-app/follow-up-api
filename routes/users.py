from typing import List
from uuid import UUID
from sqlalchemy import or_
from fastapi import APIRouter, Depends, HTTPException, File
from sqlalchemy.orm import Session
from starlette import status
from config import get_settings, Settings
from core.security import check_is_admin_user, hash_password, get_current_user
from db import get_db
from db.models import User, UserPermission, Status
from schemas.user_schemas import UserOut, UserRegisterSchemaIn, UserStoreIn, RecoveryPasswordSchemaIn, ResetPasswordSchemaIn
from fastapi.responses import FileResponse
from core.mailer import Mailer
import random
import string
from db.mongo import Mongo

router = APIRouter()

user_tag: str = "Users"


async def get_user(session: Session, email: str) -> User:
    user = User.query(session).filter_by(email=email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="user does not exists")
    return user


@router.post('/register', tags=[user_tag], summary='Create user', description='Method for create user')
async def register(user_schema: UserStoreIn, session: Session = Depends(get_db),
                   settings: Settings = Depends(get_settings)):
    user = User.query(session).filter(or_(
        User.document == user_schema.document,
        User.email == user_schema.email)).first()
    if user:
        raise HTTPException(
            status_code=403, detail="user_already_exists")

    user = User(
        company_id=user_schema.company_id,
        password_hash=hash_password(random.choice(string.ascii_uppercase)),
        fullname=user_schema.fullname,
        email=user_schema.email,
        document=user_schema.document,
        permission=user_schema.permission,
        position=user_schema.position.upper(),
        status=Status.ACTIVE
    )
    session.add(user)
    session.commit()

    mailer = Mailer()
    mailer.welcome_user(user)

    mongo = Mongo()
    mongo.welcome_app(user)

    return UserOut.from_orm(user)


@router.post('/', tags=[user_tag], summary='Create user', description='Method for create user')
async def register(user_schema: UserRegisterSchemaIn, current_user: User = Depends(check_is_admin_user), session: Session = Depends(get_db),
                   settings: Settings = Depends(get_settings)):
    user = User.query(session).filter(or_(
        User.document == user_schema.document,
        User.email == user_schema.email)).first()
    if user:
        raise HTTPException(
            status_code=403, detail="user_already_exists")

    user = User(
        company_id=current_user.company_id,
        password_hash=hash_password(random.choice(string.ascii_uppercase)),
        fullname=user_schema.fullname,
        email=user_schema.email,
        document=user_schema.document,
        permission=UserPermission.ADMIN,
        position=user_schema.position.upper(),
        status=Status.ACTIVE
    )
    session.add(user)
    session.commit()

    mailer = Mailer()
    mailer.welcome_user(user)

    mongo = Mongo()
    mongo.welcome_app(user)

    return UserOut.from_orm(user)


@router.get('/', summary='Returns users list', response_model=List[UserOut], tags=[user_tag])
async def get_all(session: Session = Depends(get_db)):
    all_itens = User.query(session).all()
    return [UserOut.from_orm(x) for x in all_itens]


@router.get('/{id}', summary='Returns user', response_model=List[UserOut], tags=[user_tag])
async def get_id(id: UUID, current_user: User = Depends(check_is_admin_user), session: Session = Depends(get_db)):
    user: User = User.query(session).filter(User.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail='route not found')

    return [UserOut.from_orm(user)]


@router.put('/{id}', summary='Update user', response_model=UserOut, tags=[user_tag])
async def update(id: UUID, user_schema: UserRegisterSchemaIn, current_user: User = Depends(check_is_admin_user), session: Session = Depends(get_db)):
    user: User = User.query(session).filter(User.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail='route not found')

    user.fullname = user_schema.fullname
    user.document = user_schema.document
    user.email = user_schema.email
    user.permission = user_schema.permission
    user.image_path = user_schema.image_path

    session.add(user)
    session.commit()

    return UserOut.from_orm(user)


@router.get("/me/", tags=[user_tag], summary="Return user logged", response_model=UserOut)
async def me(current_user: User = Depends(get_current_user)):
    result = UserOut.from_orm(current_user)
    return result


@router.get('/{id}/active', summary='Active or inactive user', response_model=List[UserOut], tags=[user_tag])
async def delete(id: UUID, current_user: User = Depends(check_is_admin_user), session: Session = Depends(get_db)):
    user: User = User.query(session).filter(User.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail='route not found')

    if user.status == Status.ACTIVE:
        user.status = Status.INACTIVE

    if user.status == Status.INACTIVE:
        user.status = Status.ACTIVE

    session.add(user)
    session.commit()

    return UserOut.from_orm(user)


@router.post('/{id}/avatar', summary='Upload avatar', tags=[user_tag])
async def create(id: UUID, file: bytes = File(...), current_user: User = Depends(check_is_admin_user), session: Session = Depends(get_db)):
    user: User = User.query(session).filter(User.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail='route not found')

    path = 'storage/users/avatar/' + str(user.id) + '.jpg'

    with open(path, 'wb') as f:
        f.write(file)

    user.image_path = path

    session.add(user)
    session.commit()

    return UserOut.from_orm(user)


@router.get('/{id}/avatar', summary='Return avatar user',  tags=[user_tag])
async def get_id(id: UUID, session: Session = Depends(get_db)):
    user: User = User.query(session).filter(User.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail='route not found')

    if user.image_path is None:
        return UserOut.from_orm(user)

    img = user.image_path
    return FileResponse(img, media_type="image/jpeg")


@router.post('/refresh-password', summary='sender link password',  tags=[user_tag])
async def update(user_schema: RecoveryPasswordSchemaIn, session: Session = Depends(get_db)):
    user: User = User.query(session).filter(
        User.email == user_schema.email).first()
    if not user:
        raise HTTPException(status_code=404, detail='user not found')

    mailer = Mailer()
    mailer.recovery_password(user)

    return UserOut.from_orm(user)


@router.put('/refresh-password/{id}', summary='password',  tags=[user_tag])
async def update(id: UUID, user_schema: ResetPasswordSchemaIn, session: Session = Depends(get_db)):
    user: User = User.query(session).filter(
        User.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail='user not found')
    
    user.password_hash = hash_password(user_schema.password)
    
    session.add(user)
    session.commit()

    mongo = Mongo()
    mongo.update_password(user)

    return UserOut.from_orm(user)
