import datetime
import enum
from uuid import UUID, uuid4
from sqlalchemy import Column, Float, String, Boolean, Enum, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, Query, relationship
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.sql.sqltypes import Date, DateTime, Integer
from sqlalchemy_utils import UUIDType


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


class Status(enum.Enum):
    ACTIVE: str = 'ATIVO'
    INACTIVE: str = 'INATIVO'


class BondPartenal(enum.Enum):
    FATHER: str = 'PAI'
    MOTHER: str = 'MÃE'
    UNCLES: str = 'TIOS'
    GRANDPARENTS: str = 'AVÓS'
    OTHERS: str = 'OUTROS'


class Genere(enum.Enum):
    FEMALE: str = 'FEMININO'
    MALE: str = 'MASCULINO'
    OTHERS: str = 'OUTRO'


class StatusContract(enum.Enum):
    ACTIVE: str = 'ATIVO'
    IN_PREPARATION: str = 'EM PREPARAÇÂO'
    INACTIVE: str = 'INATIVO'


class StatusCompany(enum.Enum):
    ACTIVE: str = 'ATIVO'
    IN_ANALYSIS: str = 'EM ANALISE'
    BLOCKED: str = 'BLOQUEADO'
    DESACATIVE: str = 'DESATIVADO'


class StatusGrid(enum.Enum):
    SCHEDULED: str = 'AGENDADO'
    IN_PROGRESS: str = 'EM ANDAMENTO'
    PAUSED: str = 'PAUSADO'
    CANCELED: str = 'CANCELADO'
    DONE: str = 'CONCLUÍDO'


class StatusSchedule(enum.Enum):
    SCHEDULED: str = 'AGENDADO'
    IN_PROGRESS: str = 'EM ANDAMENTO'
    PAUSED: str = 'PAUSADO'
    CANCELED: str = 'CANCELADO'
    DID_NOT_ATTEND: str = 'NÃO COMPARECEU'
    DONE: str = 'CONCLUÍDO'


class StatusExecuteProcedure(enum.Enum):
    IN_PROGRESS: str = 'EM ANDAMENTO'
    PAUSED: str = 'PAUSADO'
    CANCELED: str = 'CANCELADO'
    DONE: str = 'CONCLUÍDO'


class TypeHelp(enum.Enum):
    DEPENDENT: str = 'DEPENDENTE'
    INDEPENDENT: str = 'INDEPENDENTE'
    POSITIONAL: str = 'POSICIONAL'
    GESTURE: str = 'GESTUAL'
    VERBAL: str = 'VERBAL'
    PHYSICAL: str = 'FÍSICA'
    VISUAL: str = 'VISUAL'


class EventRepeat(enum.Enum):
    NO: str = 'NÃO'
    WEEK: str = 'SEMANALMENTE'
    MOUTH: str = 'MENSALMENTE'


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
    status = Column(Enum(Status), nullable=False)


class Contractor(ModelBase):
    __tablename__ = 'contractors'

    company_id = Column(UUIDType(binary=False),
                        ForeignKey(Company.id), nullable=False)
    status = Column(Enum(StatusContract), nullable=False)

    responsable = relationship(
        'ResponsibleContract', back_populates='contractor')

    address = relationship('AddressContract', back_populates='contractor')

    student = relationship('Student', back_populates='contractor')

    student_id = association_proxy('student', 'id')
    fullname = association_proxy('student', 'fullname')


class Student(ModelBase):
    __tablename__ = 'students'

    contractor_id = Column(UUIDType(binary=False),
                           ForeignKey(Contractor.id), nullable=True)

    fullname = Column(String(255), nullable=False)
    birthday = Column(Date, nullable=True)
    allergy = Column(String(20), nullable=True)
    genere = Column(Enum(Genere), nullable=False)
    document = Column(String(20), nullable=True)
    indentity_number = Column(String(100), nullable=True)
    org_exp = Column(String(10), nullable=True)
    uf_exp = Column(String(5), nullable=True)
    nationality = Column(String(20), nullable=True)
    email = Column(String(50), nullable=True)
    phone = Column(String(50), nullable=True)
    avatar = Column(String(255), nullable=True)
    informations = Column(String(500), nullable=True)
    status = Column(Enum(Status), nullable=False)

    contractor = relationship('Contractor', back_populates='student')
    schedule = relationship('Schedule', back_populates='student')
    procedures = relationship('Procedure', back_populates='student')


class ResponsibleContract(ModelBase):
    __tablename__ = 'contract_responsibles'

    contractor_id = Column(UUIDType(binary=False),
                           ForeignKey(Contractor.id), nullable=False)
    user_id = Column(UUIDType(binary=False),
                     ForeignKey(User.id), nullable=True)

    fullname = Column(String(100), nullable=False)
    birthday = Column(Date, nullable=True)
    document = Column(String(20), nullable=True)
    indentity_number = Column(String(100), nullable=True)
    org_exp = Column(String(10), nullable=True)
    uf_exp = Column(String(5), nullable=True)
    nationality = Column(String(20), nullable=True)
    email = Column(String(50), nullable=False)
    phone = Column(String(50), nullable=True)
    bond = Column(String(50), nullable=True)
    main_contract = Column(Boolean(), nullable=True)
    avatar = Column(String(255), nullable=True)

    contractor = relationship('Contractor', back_populates='responsable')
    address = relationship('AddressContract', back_populates='responsable')


class AddressContract(ModelBase):
    __tablename__ = 'contract_address'

    contractor_id = Column(
        UUIDType(binary=False), ForeignKey(Contractor.id), nullable=False)
    responsible_contract_id = Column(
        UUIDType(binary=False), ForeignKey(ResponsibleContract.id), nullable=True)

    address = Column(String(255), nullable=False)
    number = Column(Integer(), nullable=False)
    complement = Column(String(60), nullable=True)
    zip_code = Column(String(14), nullable=False)
    district = Column(String(50), nullable=False)
    city = Column(String(50), nullable=False)
    state = Column(String(2), nullable=False)

    contractor = relationship('Contractor', back_populates='address')
    responsable = relationship('ResponsibleContract', back_populates='address')
    responsable_name = association_proxy('address', 'fullname')


class SpecialtyInstructor(ModelBase):
    __tablename__ = 'specialties_instructor'

    company_id = Column(UUIDType(binary=False),
                        ForeignKey(Company.id), nullable=False)
    specialty = Column(String(100), nullable=False)

    instructor = relationship('Instructor', back_populates='specialty')


class Instructor(ModelBase):
    __tablename__ = 'instructors'

    company_id = Column(UUIDType(binary=False),
                        ForeignKey(Company.id), nullable=False)
    user_id = Column(UUIDType(binary=False),
                     ForeignKey(User.id), nullable=True)
    specialty_instructor_id = Column(UUIDType(binary=False),
                                     ForeignKey(SpecialtyInstructor.id), nullable=True)

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
    phone = Column(String(50), nullable=True)
    whats_app = Column(Boolean(), nullable=True)
    value_hour = Column(String(50), nullable=True)
    value_mouth = Column(String(50), nullable=True)
    comission = Column(String(50), nullable=True)
    avatar = Column(String(255), nullable=True)
    status = Column(Enum(Status), nullable=False)

    schedule = relationship('Schedule', back_populates='instructor')
    address = relationship('AddressInctructor', back_populates='instructor')

    specialty = relationship('SpecialtyInstructor',
                             back_populates='instructor')
    specialty_name = association_proxy('specialty', 'specialty')


class AddressInctructor(ModelBase):
    __tablename__ = 'instructor_address'

    instructor_id = Column(UUIDType(binary=False),
                           ForeignKey(Instructor.id), nullable=False)

    address = Column(String(255), nullable=False)
    number = Column(Integer(), nullable=False)
    complement = Column(String(60), nullable=True)
    zip_code = Column(String(14), nullable=False)
    district = Column(String(50), nullable=False)
    city = Column(String(50), nullable=False)
    state = Column(String(2), nullable=False)

    instructor = relationship('Instructor', back_populates='address')


class Skill(ModelBase):
    __tablename__ = 'skills'

    company_id = Column(UUIDType(binary=False),
                        ForeignKey(Company.id), nullable=False)

    name = Column(String(100), nullable=False)
    objective = Column(String(255), nullable=False)

    schedule = relationship('SkillsSchedule', back_populates='skills')


class Procedure(ModelBase):
    __tablename__ = 'procedures'

    skill_id = Column(UUIDType(binary=False),
                      ForeignKey(Skill.id), nullable=False)

    tries = Column(Integer(), nullable=False)
    goal = Column(Float(), nullable=False)
    period = Column(String(255), nullable=False)
    name = Column(String(255), nullable=True)
    objective = Column(String(1000), nullable=True)
    stimulus = Column(String(1000), nullable=True)
    answer = Column(String(1000), nullable=True)
    consequence = Column(String(1000), nullable=True)
    materials = Column(String(1000), nullable=True)
    help = Column(String(1000), nullable=True)
    student_id = Column(UUIDType(binary=False),
                        ForeignKey(Student.id), nullable=True)

    student = relationship('Student', back_populates='procedures')


class Schedule(ModelBase):
    __tablename__ = 'schedules'

    company_id = Column(UUIDType(binary=False),
                        ForeignKey(Company.id), nullable=False)
    instructor_id = Column(UUIDType(binary=False),
                           ForeignKey(Instructor.id), nullable=True)
    student_id = Column(UUIDType(binary=False),
                        ForeignKey(Student.id), nullable=True)

    event_id = Column(UUIDType(binary=False), nullable=True)
    title = Column(String(255), nullable=False)
    start = Column(DateTime, nullable=False)
    end = Column(DateTime, nullable=False)
    start_hour = Column(String(20), nullable=True)
    end_hour = Column(String(20), nullable=True)
    repeat = Column(Enum(EventRepeat), nullable=True)
    period = Column(String(20), nullable=True)
    status = Column(Enum(StatusSchedule), nullable=False)
    details = Column(String(255), nullable=True)
    student_arrival = Column(DateTime, nullable=True)
    event_begin = Column(DateTime, nullable=True)
    event_finish = Column(DateTime, nullable=True)
    event_user_id = Column(UUIDType(binary=False),
                           ForeignKey(User.id), nullable=True)
    color = Column(String(255), nullable=True)

    instructor = relationship('Instructor', back_populates='schedule')
    student = relationship('Student', back_populates='schedule')
    event = relationship('SkillsSchedule', back_populates='event')


class Execution(ModelBase):
    __tablename__ = 'executions'

    schedule_id = Column(UUIDType(binary=False),
                         ForeignKey(Schedule.id), nullable=False)

    procedure_id = Column(UUIDType(binary=False),
                          ForeignKey(Procedure.id), nullable=False)
    trie = Column(Integer(), nullable=False)
    time = Column(String(255), nullable=False)
    success = Column(Boolean(), nullable=False)
    user_id = Column(UUIDType(binary=False),
                     ForeignKey(User.id), nullable=False)
    help_type = Column(Enum(TypeHelp), nullable=False)


class SkillsSchedule(ModelBase):
    __tablename__ = 'skills_schedules'

    schedule_id = Column(UUIDType(binary=False),
                         ForeignKey(Schedule.id), nullable=False)
    skill_id = Column(UUIDType(binary=False),
                      ForeignKey(Skill.id), nullable=False)
    finished = Column(Boolean, default=False, nullable=True)

    skills = relationship('Skill', back_populates='schedule')
    event = relationship('Schedule', back_populates='event')

    skill_name = association_proxy('skills', 'name')
