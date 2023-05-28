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
    updated_at = Column(DateTime, default=datetime.datetime.now,
                        onupdate=datetime.datetime.now)

    @classmethod
    def query(cls, session: Session) -> Query:
        return session.query(cls).filter(cls.deleted == False)


class UserPermission(enum.Enum):
    ADMIN: str = 'ADMIN'
    INSTRUCTOR: str = 'INSTRUCTOR'
    PARENTS: str = 'PARENTS'
    STUDANTS: str = 'STUDANTS'


class UserFunction(enum.Enum):
    ADMIN: str = 'GERENTE'
    ENGINEER: str = 'ENGENHEIRO'
    ABA: str = 'ABA'
    PSYCHOLOGIST: str = 'PSICÓLOGA'
    PSYCHOPEDAGOGUE: str = 'PSICOPEDAGOGA'
    PHONO: str = 'FONO'
    FINANCIAL: str = 'FINANCEIRO'
    PARENT: str = 'RESPONSÁVEL'
    STUDANT: str = 'ALUNO'

class StatusContract(enum.Enum):
    ACTIVE: str = 'ATIVO'
    INACTIVE: str = 'INATIVO'

class StatusInstructor(enum.Enum):
    ACTIVE: str = 'ATIVO'
    INACTIVE: str = 'INATIVO'

class StatusBankAccount(enum.Enum):
    ACTIVE: str = 'ATIVO'
    INACTIVE: str = 'INATIVO'


class StatusCompany(enum.Enum):
    ACTIVE: str = 'ATIVO'
    IN_ANALYSIS: str = 'EM ANALISE'
    BLOCKED: str = 'BLOQUEADO'
    DESACATIVE: str = 'DESATIVADO'


class StatusGrid(enum.Enum):
    IN_PROGRESS: str = 'EM ANDAMENTO'
    PAUSED: str = 'PAUSADO'
    CANCELED: str = 'CANCELADO'
    DONE: str = 'CONCLUÍDO'


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

    company_id = Column(UUIDType(binary=False),
                        ForeignKey(Company.id), nullable=False)

    fullname = Column(String(100), nullable=False)
    password_hash = Column(String(100), nullable=False)
    email = Column(String(50), nullable=False, unique=True)
    document = Column(String(20), nullable=True)
    permission = Column(Enum(UserPermission), nullable=False)
    image_path = Column(String(100), nullable=True)
    position = Column(String(100), nullable=True)


class Contractor(ModelBase):
    __tablename__ = 'contractors'

    company_id = Column(UUIDType(binary=False),
                        ForeignKey(Company.id), nullable=False)
    status = Column(Enum(StatusContract), nullable=False)

    responsible = relationship(
        'ResponsibleContract', back_populates='contract')
    responsible_name = relationship(
        'ResponsibleContract', back_populates='contract')

    student = relationship('Student', back_populates='contract')
    student_name = association_proxy('student', 'fullname')


class ResponsibleContract(ModelBase):
    __tablename__ = 'contract_responsibles'

    contractor_id = Column(UUIDType(binary=False),
                           ForeignKey(Contractor.id), nullable=False)
    user_id = Column(UUIDType(binary=False),
                     ForeignKey(User.id), nullable=True)

    fullname = Column(String(100), nullable=False)
    document = Column(String(20), nullable=True)
    indentity_number = Column(String(20), nullable=True)
    email = Column(String(50), nullable=True)

    contract = relationship('Contractor', back_populates='responsible')


class AddressContract(ModelBase):
    __tablename__ = 'contract_address'

    responsible_contract_id = Column(
        UUIDType(binary=False), ForeignKey(Contractor.id), nullable=False)
    
    address = Column(String(255), nullable=False)
    complement = Column(String(10), nullable=False)
    zip_code = Column(String(14), nullable=False)
    district = Column(String(50), nullable=False)
    city = Column(String(50), nullable=False)
    state = Column(String(2), nullable=False)


class Student(ModelBase):
    __tablename__ = 'students'

    contractor_id = Column(UUIDType(binary=False),
                           ForeignKey(Contractor.id), nullable=True)
    instructor_id = Column(UUIDType(binary=False),
                           ForeignKey(User.id), nullable=True)

    fullname = Column(String(255), nullable=False)
    birthday = Column(Date, nullable=True)
    avatar = Column(String(255), nullable=True)

    grids = relationship('Grid', back_populates='student')
    contract = relationship('Contractor', back_populates='student')

class SpecialtyInstructor(ModelBase):
    __tablename__ = 'specialties_instructor'

    company_id = Column(UUIDType(binary=False),
                        ForeignKey(Company.id), nullable=False)
    specialty = Column(String(100), nullable=False)


class Instructor(ModelBase):
    __tablename__ = 'instructors'

    company_id = Column(UUIDType(binary=False),
                        ForeignKey(Company.id), nullable=False)
    user_id = Column(UUIDType(binary=False),
                     ForeignKey(User.id), nullable=True)
    specialty_instructor_id = Column(UUIDType(binary=False),
                     ForeignKey(SpecialtyInstructor.id), nullable=False)
    
    fullname = Column(String(100), nullable=False)
    document = Column(String(100), nullable=False)
    indentity_number = Column(String(100), nullable=True)
    org_exp = Column(String(10), nullable=True)
    uf_exp = Column(String(5), nullable=True)
    nationality = Column(String(20), nullable=True)
    birthday = Column(Date, nullable=True)
    document_company = Column(String(20), nullable=True)
    social_name = Column(String(100), nullable=True)
    fantasy_name = Column(String(100), nullable=True)
    email = Column(String(50), nullable=False)
    phone: Column(String(50), nullable=True)
    value_hour = Column(String(50), nullable=True)
    value_mouth = Column(String(50), nullable=True)
    comission: Column(String(50), nullable=True)
    avatar = Column(String(255), nullable=True)
    status = Column(Enum(StatusContract), nullable=False)

    grids = relationship('Grid', back_populates='instructor')

class AddressInctructor(ModelBase):
    __tablename__ = 'instructor_address'

    instructor_id = Column(UUIDType(binary=False),
                           ForeignKey(Instructor.id), nullable=False)

    address = Column(String(255), nullable=False)
    complement = Column(String(10), nullable=False)
    zip_code = Column(String(14), nullable=False)
    district = Column(String(50), nullable=False)
    city = Column(String(50), nullable=False)
    state = Column(String(2), nullable=False)


class BankAccountInstructor(ModelBase):
    __tablename__ = 'instructor_bank_accounts'

    instructor_id = Column(UUIDType(binary=False),
                           ForeignKey(Instructor.id), nullable=False)
    
    bank_code = Column(Integer(), nullable=False)
    bank_name = Column(String(255), nullable=False)
    agency = Column(Integer(), nullable=False)
    account_number = Column(Integer(), nullable=False)
    account_type = Column(String(255), nullable=False)
    status = Column(Enum(StatusBankAccount), nullable=False)


class Program(ModelBase):
    __tablename__ = 'programs'

    company_id = Column(UUIDType(binary=False),
                        ForeignKey(Company.id), nullable=False)

    title = Column(String(100), nullable=False)
    description = Column(String(255), nullable=False)

    procedures = relationship('Procedure', back_populates='program')
    grids = relationship('Grid', back_populates='program')


class Procedure(ModelBase):
    __tablename__ = 'procedures'

    program_id = Column(UUIDType(binary=False),
                        ForeignKey(Program.id), nullable=False)
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

    program_id = Column(UUIDType(binary=False),
                        ForeignKey(Program.id), nullable=False)
    student_id = Column(UUIDType(binary=False),
                        ForeignKey(Student.id), nullable=False)
    instructor_id = Column(UUIDType(binary=False),
                           ForeignKey(Instructor.id), nullable=True)

    date_schedule = Column(DateTime, nullable=True)
    time_preview = Column(String(20), nullable=True)
    observation = Column(String(255), nullable=True)
    date_start = Column(DateTime, nullable=True)
    date_finish = Column(DateTime, nullable=True)
    status = Column(Enum(StatusGrid), nullable=False)

    program = relationship('Program', back_populates='grids')
    program_title = association_proxy('program', 'title')

    student = relationship('Student', back_populates='grids')
    student_name = association_proxy('student', 'fullname')

    instructor = relationship('Instructor', back_populates='grids')
    instructor_name = association_proxy('instructor', 'fullname')


class Result(ModelBase):
    __tablename__ = 'results'

    procedure_id = Column(UUIDType(binary=False),
                          ForeignKey(Procedure.id), nullable=False)
    student_id = Column(UUIDType(binary=False),
                        ForeignKey(Student.id), nullable=False)
    instructor_id = Column(UUIDType(binary=False),
                           ForeignKey(Instructor.id), nullable=True)

    attempts = Column(Integer(), nullable=True)
    points_made = Column(String(255), nullable=False)
    anotations = Column(String(255), nullable=True)
    date_start = Column(DateTime, nullable=True)
    date_finish = Column(DateTime, nullable=True)
