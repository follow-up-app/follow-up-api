from curses.textpad import Textbox
from datetime import date
import datetime
import enum
from typing import List, Text
from uuid import UUID, uuid4
from sqlalchemy import Column, Float, String, Boolean, Enum, ForeignKey
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
    parent = Column(UUIDType(binary=False), ForeignKey(User.id), nullable=True)
    instructor = Column(UUIDType(binary=False), ForeignKey(User.id), nullable=True)

    fullname = Column(String(255), nullable=False)
    birthday = Column(Date, nullable=True)
    avatar = Column(String(255), nullable=True)
    age = Column(String(3), nullable=True)

    grids = relationship('Grid', back_populates='student')


class Program(ModelBase):
    __tablename__ = 'programs'

    company_id = Column(UUIDType(binary=False), ForeignKey(Company.id), nullable=False)

    title = Column(String(255), nullable=False)
    description = Column(String(255), nullable=False)

    procedures = relationship('Procedure', back_populates='program')
    grids = relationship('Grid', back_populates='program')



class Procedure(ModelBase):
    __tablename__ = 'procedures'

    program_id = Column(UUIDType(binary=False), ForeignKey(Program.id), nullable=False)
    name = Column(String(255), nullable=True)
    objective = Column(String(1000), nullable=True)
    stimulus = Column(String(1000), nullable=True)
    answer = Column(String(1000), nullable=True)
    consequence = Column(String(1000), nullable=True)
    material = Column(String(1000), nullable=True)
    type_help = Column(String(1000), nullable=True)
    attempts = Column(Integer(), nullable=True)
    goal_value = Column(String(255), nullable=True)
    description = Column(String(1000), nullable=True)

    program = relationship('Program', back_populates='procedures')
    program_title = association_proxy('program', 'title')



class Grid(ModelBase):
    __tablename__ = 'grids'

    program_id = Column(UUIDType(binary=False), ForeignKey(Program.id), nullable=False)
    student_id = Column(UUIDType(binary=False), ForeignKey(Student.id), nullable=False)
    
    aplicator = Column(UUIDType(binary=False), ForeignKey(User.id), nullable=True)
    status = Column(Enum(StatusGrid), nullable=False)

    program = relationship('Program', back_populates='grids')
    program_title = association_proxy('program', 'title')

    student = relationship('Student', back_populates='grids')
    student_name = association_proxy('student', 'fullname')



class Result(ModelBase):
    __tablename__ = 'results'

    procedure_id = Column(UUIDType(binary=False), ForeignKey(Procedure.id), nullable=False)
    student_id = Column(UUIDType(binary=False), ForeignKey(Student.id), nullable=False)
    attempts = Column(Integer(), nullable=True)
    points_made = Column(String(255), nullable=False)
    anotations = Column(String(255), nullable=True)