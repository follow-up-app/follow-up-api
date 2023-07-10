from datetime import date
from typing import Optional, List
from uuid import UUID
from pydantic import BaseModel
from db.models import Status


class SkillIn(BaseModel):
    name: str
    objective: str


class SkillOut(BaseModel):
    id: UUID
    name: str
    objective: str

    class Config:
        orm_mode = True