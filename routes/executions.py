from datetime import timedelta
from typing import List
from uuid import UUID
from sqlalchemy import or_
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.security import get_current_user
from db import get_db
from db.models import Execution, User, Procedure
from schemas.execution_schemas import ExecutionIn, ExecutionOut

router = APIRouter()

tags: str = "Exceution"


@router.post('/', summary='Create execution', tags=[tags], response_model=ExecutionOut)
async def create(execute_in: ExecutionIn, current_user: User = Depends(get_current_user), session: Session = Depends(get_db)):
    procedure: Procedure = Procedure.query(session).filter(
        Procedure.id == execute_in.procedure_id).first()

    if not procedure:
        raise HTTPException(status_code=404, detail='procedure not found')

    tries: Execution = Execution.query(session).filter(
        Execution.schedule_id == execute_in.schedule_id, Execution.procedure_id == execute_in.procedure_id).count()

    if tries >= execute_in.trie or execute_in.trie > procedure.tries:
        raise HTTPException(
            status_code=406, detail='tries of procedure exceeded')

    execution = Execution(
        schedule_id=execute_in.schedule_id,
        procedure_id=execute_in.procedure_id,
        trie=execute_in.trie,
        time=execute_in.time,
        help_type=execute_in.help_type,
        user_id=current_user.id,
        success=True,
    )
    session.add(execution)
    session.commit()

    return ExecutionOut.from_orm(execution)


@router.get('/{schedule_id}/{procedure_id}', summary='Return execution list for scheduled', response_model=List[ExecutionOut], tags=[tags])
async def get_all(schedule_id: UUID, procedure_id: UUID, current_user: User = Depends(get_current_user), session: Session = Depends(get_db)):
    all_itens: Execution = Execution.query(session).filter(
        Execution.schedule_id == schedule_id, Execution.procedure_id == procedure_id).all()
    return [ExecutionOut.from_orm(x) for x in all_itens]


@router.get('/{id}', summary='Return execution list for scheduled', response_model=ExecutionOut, tags=[tags])
async def get_all(id: UUID, current_user: User = Depends(get_current_user), session: Session = Depends(get_db)):
    execution: Execution = Execution.query(
        session).filter(Execution.id == id).first()
    if not execution:
        raise HTTPException(status_code=404, detail='execution not found')

    return ExecutionOut.from_orm(execution)
