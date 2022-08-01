from datetime import timedelta
from typing import List
from uuid import UUID
from sqlalchemy import or_
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from itsdangerous import URLSafeTimedSerializer
from sqlalchemy.orm import Session
from starlette import status
from starlette.background import BackgroundTasks
import re
import os
import unidecode
from config import get_settings, Settings
from core.security import check_is_admin_user, check_is_parents_user, hash_password, verify_password, create_access_token, get_current_user
from db import get_db
from db.models import Grid, StatusGrid, Student, User
from schemas.grid_schemas import GridIn, GridOut

router = APIRouter()

tags: str = "Grid"

@router.post('/', summary='Create grid', response_model=GridOut, tags=[tags])
async def create(grid_in: GridIn, current_user: User = Depends(check_is_admin_user), session: Session = Depends(get_db)):
    student: Student = Student.query(session).filter(Student.id == grid_in.student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail='route not found')    
    
    grid = Grid(
        program_id=grid_in.program_id,
        student_id=grid_in.student_id,
        aplicator=student.instructor,
        status=StatusGrid.IN_PROGRESS,
    )
    session.add(grid)
    session.commit()

    return GridOut.from_orm(grid)


@router.get('/', summary='Returns grid list', response_model=List[GridOut], tags=[tags])
async def get_all(current_user: User = Depends(check_is_admin_user), session: Session = Depends(get_db)):
    all_itens = Grid.query(session).all()
    return [GridOut.from_orm(x) for x in all_itens]


@router.get('/student/{id}', summary='Returns grid list', response_model=List[GridOut], tags=[tags])
async def get_all(id: UUID, current_user: User = Depends(check_is_admin_user), session: Session = Depends(get_db)):
    all_itens = Grid.query(session).filter(Grid.student_id == id).all()
    return [GridOut.from_orm(x) for x in all_itens]


@router.get('/{id}', summary='Returns grid', response_model=List[GridOut], tags=[tags])
async def get_id(id: UUID, current_user: User = Depends(check_is_admin_user), session: Session = Depends(get_db)):
    grid: Grid = Grid.query(session).filter(Grid.id == id).first()
    if not grid:
        raise HTTPException(status_code=404, detail='route not found')

    return [GridOut.from_orm(grid)]


@router.delete('/{id}', summary='Delete grid', response_model=List[GridOut], tags=[tags])
async def delete(id: UUID, current_user: User = Depends(check_is_admin_user), session: Session = Depends(get_db)):
    grid: Grid = Grid.query(session).filter(Grid.id == id).first()
    if not grid:
        raise HTTPException(status_code=404, detail='route not found')
    session.delete(grid)
    session.commit()
