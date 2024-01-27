from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.security import get_current_user
from db import get_db
from db.models import User, Schedule, Skill, Execution, TypeHelp
from schemas.schedule_schemas import ScheduleOut
from datetime import datetime
from schemas.follow_up_schemas import ScheduleFollowUp, Filters

router = APIRouter()

tags: str = "Follow-up"


@router.get('/', summary='Return follow-up list', response_model=List[ScheduleOut], tags=[tags])
async def get_all(current_user: User = Depends(get_current_user), session: Session = Depends(get_db)):
    all_itens = Schedule.query(session).order_by(
        Schedule.updated_at.desc()).all()
    return [ScheduleOut.from_orm(x) for x in all_itens]


@router.get('/schedule/{id}', summary='Return result details', tags=[tags])
async def get_id(id: UUID, current_user: User = Depends(get_current_user), session: Session = Depends(get_db)):
    schedule: Schedule = Schedule.query(
        session).filter(Schedule.id == id).first()
    if not schedule:
        raise HTTPException(status_code=404, detail='schedule not found')

    skil: Skill = Skill.query(session).filter(
        Skill.id == schedule.skill_id).first()
    if not skil:
        raise HTTPException(status_code=404, detail='skill not found')

    results = []
    executions = []
    for procedure in skil.procedures:
        procedure.points = 0
        executions: Execution = Execution.query(session).filter(
            Execution.procedure_id == procedure.id, 
            Execution.schedule_id == id).order_by(Execution.trie).all()
        if executions:
            procedure.points = round(Execution.query(session).filter(
                Execution.procedure_id == procedure.id,
                Execution.schedule_id == id,
                Execution.help_type == TypeHelp.INDEPENDENT).count() / procedure.tries * 100, 2)
            procedure.executions = executions
            results.append(procedure)

    schedule.results = results
    return ScheduleFollowUp.from_orm(schedule)


@router.get('/mobile-schedule/{id}', summary='Return result details', tags=[tags])
async def get_id(id: UUID, current_user: User = Depends(get_current_user), session: Session = Depends(get_db)):
    schedule: Schedule = Schedule.query(
        session).filter(Schedule.id == id).first()
    if not schedule:
        raise HTTPException(status_code=404, detail='schedule not found')

    skil: Skill = Skill.query(session).filter(
        Skill.id == schedule.skill_id).first()
    if not skil:
        raise HTTPException(status_code=404, detail='skill not found')

    for procedure in skil.procedures:
        executions: Execution = Execution.query(session).filter(
            Execution.procedure_id == procedure.id, Execution.schedule_id == id).count()

        procedure.total_exec = int(executions)
        procedure.data_chart = round(executions / procedure.tries, 2)

        procedure.app_active = True
        if executions >= procedure.tries:
            procedure.app_active = False

    return ScheduleFollowUp.from_orm(schedule)


@router.post('/filters/', summary='Return result details', tags=[tags])
async def get_filters(filters: Filters, current_user: User = Depends(get_current_user), session: Session = Depends(get_db)):
    start = datetime.combine(filters.start, datetime.min.time())
    end = datetime.combine(filters.end, datetime.max.time())

    schedules = Schedule.query(session).filter(Schedule.start >= start,
                                               Schedule.start <= end)
    if filters.student_id is not None:
        all_itens = schedules.filter(
            Schedule.student_id == filters.student_id).all()

    else:
        all_itens = schedules.all()

    return [ScheduleOut.from_orm(x) for x in all_itens]


@router.get('/student/{id}', summary='Return result details', tags=[tags])
async def get_id(id: UUID, current_user: User = Depends(get_current_user), session: Session = Depends(get_db)):
    schedule: Schedule = Schedule.query(
        session).filter(Schedule.id == id).first()
    if not schedule:
        raise HTTPException(status_code=404, detail='schedule not found')

    return ScheduleOut.from_orm(schedule)
