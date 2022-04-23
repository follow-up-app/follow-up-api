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

    fullname = Column(String(255), nullable=False)
    password_hash = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    document = Column(String(255), nullable=True)
    permission = Column(Enum(UserPermission), nullable=False)