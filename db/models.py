from datetime import date
import datetime
import enum
from typing import List
from uuid import UUID, uuid4
from sqlalchemy import Column, String, Boolean, Enum, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, Query, relationship
from sqlalchemy.sql.expression import column, false, null
from sqlalchemy.sql.schema import Table, UniqueConstraint
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.sql.sqltypes import Date, DateTime, Integer
from sqlalchemy_utils import UUIDType

import pytz




Base = declarative_base()


class ModelBase(Base):
    __abstract__ = True

    id = Column(UUIDType(binary=False), primary_key=True, default=uuid4)
    deleted = Column(Boolean, default=False, nullable=False)
    created_date = Column(DateTime, default=datetime.datetime.now)
    updated_at = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)
    
    @classmethod
    def query(cls, session: Session) -> Query:
        return session.query(cls).filter(cls.deleted == False)
    

class UserPermission(enum.Enum):
    ADMIN: str = 'ADMIN'
    INSTRUCTOR: str = 'INSTRUCTOR'
    PARENTS: str = 'PARENTS'
    STUDANTS: str = 'STUDANTS'


class StatusCompany(enum.Enum):
    ACTIVE: str = 'ACTIVE'
    IN_ANALYSIS: str = 'IN_ANALYSIS'
    BLOCKED: str = 'BLOCKED'
    DESACATIVE: str = 'DESACATIVE'


class MarkProcedure(enum.Enum):
    PLAY: str = 'BRINCAR'
    ECHOIC: str = 'ECOICO'
    WRITING: str = 'ESCRITA'
    GROUP: str = 'GRUPO'
    IMITATION: str = 'IMITAÇÃO'
    INTRAVERBAL: str = 'INTRAVERBAL'
    READING: str = 'LEITURA'
    LINGUISTICS: str = 'LINGUISTICA'
    LRFFC: str = 'LRFFC'
    COMMAND: str = 'MANDO'
    MATHEMATICS: str = 'MATEMÁTICA'
    LISTENER: str = 'OUVINTE'
    PV_MTS: str = 'PV-MTS'
    SOCIAL: str = 'SOCIAL'
    TACT: str = 'TATO'
    VOCAL: str = 'VOCAL'


class StatusGrid(enum.Enum):
    IN_PROGRESS: str = 'IN_PROGRESS'
    PAUSED: str = 'PAUSED'
    CANCELED: str = 'CANCELED'
    DONE: str = 'DONE'


class Company(ModelBase):
    __tablename__ = 'companies'

    name = Column(String(255), nullable=False)
    document = Column(String(255), nullable=False)
    address = Column(String(255), nullable=False)
    complement = Column(String(255), nullable=True)
    zip_code = Column(String(255), nullable=False)
    city = Column(String(255), nullable=False)
    state = Column(String(255), nullable=False)
    country = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    phone = Column(String(255), nullable=False)
    status = Column(Enum(StatusCompany), nullable=False)


class User(ModelBase):
    __tablename__ = 'users'

    company_id = Column(UUIDType(binary=False), ForeignKey(Company.id), nullable=False)

    fullname = Column(String(255), nullable=False)
    password_hash = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    document = Column(String(255), nullable=True)
    permission = Column(Enum(UserPermission), nullable=False)


class Student(ModelBase):
    __tablename__ = 'students'

    company_id = Column(UUIDType(binary=False), ForeignKey(Company.id), nullable=False)
    parent = Column(UUIDType(binary=False), ForeignKey(User.id), nullable=False)

    fullname = Column(String(255), nullable=False)
    age: Column(String(255), nullable=False)


class Program(ModelBase):
    __tablename__ = 'programs'

    company_id = Column(UUIDType(binary=False), ForeignKey(Company.id), nullable=False)

    title = Column(String(255), nullable=False)
    objective = Column(String(255), nullable=False)


class Procedure(ModelBase):
    __tablename__ = 'procedures'

    program_id = Column(UUIDType(binary=False), ForeignKey(Program.id), nullable=False)

    mark = Column(Enum(MarkProcedure), nullable=False)
    level = Column(Integer(), nullable=False)
    stimulus = Column(String(255), nullable=False)
    orientation_executation = Column(String(255), nullable=False)
    orientation_partial_executation = Column(String(255), nullable=True)
    points_total = Column(Integer(), nullable=False)
    points_partial = Column(Integer(), nullable=True)


class Grid(ModelBase):
    __tablename__ = 'grids'

    program_id = Column(UUIDType(binary=False), ForeignKey(Program.id), nullable=False)
    student_id = Column(UUIDType(binary=False), ForeignKey(Student.id), nullable=False)
    aplicator = Column(UUIDType(binary=False), ForeignKey(User.id), nullable=False)
    
    status = Column(Enum(StatusGrid), nullable=False)



class Result(ModelBase):
    __tablename__ = 'results'

    procedure_id = Column(UUIDType(binary=False), ForeignKey(Procedure.id), nullable=False)
    student_id = Column(UUIDType(binary=False), ForeignKey(Student.id), nullable=False)
    
    points_made = Column(Integer, nullable=False)
    anotations = Column(String(255), nullable=True)