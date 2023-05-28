from datetime import timedelta
from typing import List
from uuid import UUID
from sqlalchemy import or_
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from itsdangerous import URLSafeTimedSerializer
from sqlalchemy.orm import Session
from config import get_settings, Settings
from core.security import check_is_admin_user, check_is_parents_user, hash_password, verify_password, create_access_token, get_current_user
from db import get_db
from db.models import Result, User, Procedure
from schemas.result_schemas import ResultIn, ResultOut


router = APIRouter()

tags: str = "Results"


@router.post('/', summary='Create result of procedure', response_model=List[ResultOut], tags=[tags])
async def create(result_in: ResultIn, current_user: User = Depends(check_is_admin_user), session: Session = Depends(get_db)):
    proceduce: Procedure = Procedure.query(session).filter(
        Procedure.id == result_in.procedure_id).first()
    if not proceduce:
        raise HTTPException(status_code=404, detail='route not found')

    points_made = result_in.attempts / proceduce.attempts

    result = Result(
        procedure_id=result_in.procedure_id,
        student_id=result_in.student_id,
        points_made=points_made,
        attempts=result_in.attempts,
        anotations=result_in.procedure_id,
        date_start=result_in.date_start,
        date_finish=result_in.date_finish,
    )
    session.add(result)
    session.commit()

    return ResultOut.from_orm(result)


@router.get('/', summary='Returns results list', response_model=List[ResultOut], tags=[tags])
async def get_all(current_user: User = Depends(check_is_parents_user), session: Session = Depends(get_db)):
    all_itens = Result.query(session).all()
    return [ResultOut.from_orm(x) for x in all_itens]


@router.get('/{id}', summary='Returns result of procedure', tags=[tags])
async def get_id(id: UUID, current_user: User = Depends(check_is_parents_user), session: Session = Depends(get_db)):
    result: Result = Result.query(session).filter(Result.id == id).first()
    if not result:
        raise HTTPException(status_code=404, detail='route not found')

    return [ResultOut.from_orm(result)]


@router.put('/{id}', summary='Update result of procedure', response_model=ResultOut, tags=[tags])
async def update(id: UUID, result_in: ResultIn, current_user: User = Depends(check_is_admin_user), session: Session = Depends(get_db)):
    result: Result = Result.query(session).filter(Result.id == id).first()
    if not result:
        raise HTTPException(status_code=404, detail='route not found')
    
    proceduce: Procedure = Procedure.query(session).filter(
        Procedure.id == result_in.procedure_id).first()
    if not proceduce:
        raise HTTPException(status_code=404, detail='route not found')
    
    points_made = result_in.attempts / proceduce.attempts
    
    result.attempts = result_in.attempts
    result.points_made = points_made
    result.date_start = result_in.date_start
    result.date_finish = result_in.date_finish
    
    session.add(result)
    session.commit()

    return ResultOut.from_orm(result)
