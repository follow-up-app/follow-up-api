import datetime
from uuid import uuid4
from sqlalchemy import Column, Float, String, Boolean, Enum, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, Query, relationship
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.sql.sqltypes import Date, DateTime, Integer
from sqlalchemy_utils import UUIDType
from app.constants.enums.company_enum import CompanyEnum
from app.constants.enums.contract_enum import ContractEnum
from app.constants.enums.genere_enum import GenereEnum
from app.constants.enums.help_enum import HelpEnum
from app.constants.enums.partenal_enum import PartenalEnum
from app.constants.enums.permission_enum import PermissionEnum
from app.constants.enums.repeat_enum import RepeatEnum
from app.constants.enums.schedule_enum import ScheduleEnum
from app.constants.enums.status_enum import StatusEnum
from app.constants.enums.payment_enum import PaymentEnum, OrderPaymentEnum
from app.constants.enums.instructor_payments_enum import ModePaymentEnum, TypePaymentEnum
from app.constants.enums.billing_enum import BillingEnum, CategoryEnum
from app.constants.enums.invoice_enum import InvoiceSenderStatusEnum

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


class Company(ModelBase):
    __tablename__ = 'companies'

    name = Column(String(255), nullable=True)
    social_name = Column(String(255), nullable=True)
    fantasy_name = Column(String(255), nullable=True)
    document = Column(String(255), nullable=False)
    municipal_registration = Column(String(50), nullable=True)
    address = Column(String(255), nullable=False)
    number_address = Column(Integer(), nullable=True)
    complement = Column(String(20), nullable=True)
    zip_code = Column(String(20), nullable=False)
    district = Column(String(255), nullable=True)
    city = Column(String(100), nullable=False)
    state = Column(String(10), nullable=False)
    city_code = Column(String(50), nullable=True)
    email = Column(String(255), nullable=False)
    phone = Column(String(255), nullable=False)
    aliquot = Column(String(50), nullable=True)
    item_list_service = Column(String(50), nullable=True)
    municipal_tax_code = Column(String(50), nullable=True)
    iss_retained = Column(Boolean(), nullable=True)
    api_nfes_token = Column(String(50), nullable=True)
    licences_n = Column(Integer(), nullable=True)
    status = Column(Enum(CompanyEnum), nullable=False)

    users = relationship('User', back_populates='company')


class User(ModelBase):
    __tablename__ = 'users'

    company_id = Column(UUIDType(binary=False),
                        ForeignKey(Company.id), nullable=False)

    fullname = Column(String(100), nullable=False)
    password_hash = Column(String(100), nullable=False)
    email = Column(String(50), nullable=False, unique=True)
    document = Column(String(20), nullable=True)
    permission = Column(Enum(PermissionEnum), nullable=False)
    image_path = Column(String(100), nullable=True)
    position = Column(String(100), nullable=True)
    status = Column(Enum(StatusEnum), nullable=False)

    company = relationship('Company', back_populates='users')


class Specialty(ModelBase):
    __tablename__ = 'specialties'

    company_id = Column(UUIDType(binary=False),
                        ForeignKey(Company.id), nullable=False)
    name = Column(String(100), nullable=False)
    description = Column(String(100), nullable=False)
    code_nfes = Column(String(100), nullable=True)
    value_hour = Column(Float(), nullable=False)

    instructor = relationship('Instructor', back_populates='specialty')
    schedule = relationship('Schedule', back_populates='specialty')
    skills = relationship('Skill', back_populates='specialty')


class Contractor(ModelBase):
    __tablename__ = 'contractors'

    company_id = Column(UUIDType(binary=False),
                        ForeignKey(Company.id), nullable=False)

    type_billing = Column(Enum(CategoryEnum), nullable=True)
    status = Column(Enum(ContractEnum), nullable=False)

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
    genere = Column(Enum(GenereEnum), nullable=False)
    document = Column(String(20), nullable=True)
    indentity_number = Column(String(100), nullable=True)
    org_exp = Column(String(10), nullable=True)
    uf_exp = Column(String(5), nullable=True)
    nationality = Column(String(20), nullable=True)
    email = Column(String(50), nullable=True)
    phone = Column(String(50), nullable=True)
    avatar = Column(String(255), nullable=True)
    informations = Column(String(500), nullable=True)
    status = Column(Enum(StatusEnum), nullable=False)

    contractor = relationship('Contractor', back_populates='student')
    schedule = relationship('Schedule', back_populates='student')
    procedures = relationship('Procedure', back_populates='student')
    billing = relationship('Billing', back_populates='student')


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
    bond = Column(Enum(PartenalEnum), nullable=True)
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
    city_code = Column(String(255), nullable=True)

    contractor = relationship('Contractor', back_populates='address')
    responsable = relationship('ResponsibleContract', back_populates='address')
    responsable_name = association_proxy('address', 'fullname')


class Instructor(ModelBase):
    __tablename__ = 'instructors'

    company_id = Column(UUIDType(binary=False),
                        ForeignKey(Company.id), nullable=False)
    user_id = Column(UUIDType(binary=False),
                     ForeignKey(User.id), nullable=True)
    specialty_id = Column(UUIDType(binary=False),
                          ForeignKey(Specialty.id), nullable=True)

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
    crp = Column(String(50), nullable=True)
    email = Column(String(50), nullable=False)
    phone = Column(String(50), nullable=True)
    whats_app = Column(Boolean(), nullable=True)
    comission = Column(String(50), nullable=True)
    avatar = Column(String(255), nullable=True)
    status = Column(Enum(StatusEnum), nullable=False)
    type_payment = Column(Enum(TypePaymentEnum), nullable=True)
    mode_payment = Column(Enum(ModePaymentEnum), nullable=True)
    value = Column(Float(), nullable=True)

    specialty = relationship('Specialty', back_populates='instructor')
    schedule = relationship('Schedule', back_populates='instructor')
    address = relationship('AddressInstructor', back_populates='instructor')
    payment_details = relationship(
        'IntructorPaymentsDetail', back_populates='instructor')
    payment = relationship('Payment', back_populates='instructor')
    order_payments = relationship('OrderPayment', back_populates='instructor')

    specialty_name = association_proxy('specialty', 'name')


class AddressInstructor(ModelBase):
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


class IntructorPaymentsDetail(ModelBase):
    __tablename__ = 'instructor_payment_details'

    instructor_id = Column(UUIDType(binary=False),
                           ForeignKey(Instructor.id), nullable=False)

    bank_number = Column(Integer(), nullable=True)
    bank_branch = Column(Integer(), nullable=True)
    account_number = Column(String(50), nullable=True)
    key = Column(String(255), nullable=True)

    instructor = relationship('Instructor', back_populates='payment_details')


class Skill(ModelBase):
    __tablename__ = 'skills'

    company_id = Column(UUIDType(binary=False),
                        ForeignKey(Company.id), nullable=False)
    specialty_id = Column(UUIDType(binary=False),
                          ForeignKey(Specialty.id), nullable=True)

    name = Column(String(100), nullable=False)
    objective = Column(String(255), nullable=False)

    schedule = relationship('SkillsSchedule', back_populates='skills')
    procedure = relationship('ProcedureSchedule', back_populates='skills')
    specialty = relationship('Specialty', back_populates='skills')

    specialty_name = association_proxy('specialty', 'name')


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


class Event(ModelBase):
    __tablename__ = 'events'

    company_id = Column(UUIDType(binary=False),
                        ForeignKey(Company.id), nullable=False)
    student_id = Column(UUIDType(binary=False),
                        ForeignKey(Student.id), nullable=True)

    start_in = Column(DateTime, nullable=False)
    repeat = Column(Enum(RepeatEnum), nullable=True)
    period = Column(String(20), nullable=True)


class Schedule(ModelBase):
    __tablename__ = 'schedules'

    company_id = Column(UUIDType(binary=False),
                        ForeignKey(Company.id), nullable=False)
    instructor_id = Column(UUIDType(binary=False),
                           ForeignKey(Instructor.id), nullable=True)
    student_id = Column(UUIDType(binary=False),
                        ForeignKey(Student.id), nullable=True)
    specialty_id = Column(UUIDType(binary=False),
                          ForeignKey(Specialty.id), nullable=True)
    event_id = Column(UUIDType(binary=False),
                          ForeignKey(Event.id), nullable=True)

    title = Column(String(255), nullable=False)
    start = Column(DateTime(timezone=True), nullable=False)
    end = Column(DateTime, nullable=False)
    start_hour = Column(String(20), nullable=True)
    end_hour = Column(String(20), nullable=True)
    repeat = Column(Enum(RepeatEnum), nullable=True)
    period = Column(String(20), nullable=True)
    status = Column(Enum(ScheduleEnum), nullable=False)
    details = Column(String(255), nullable=True)
    student_arrival = Column(DateTime, nullable=True)
    event_begin = Column(DateTime, nullable=True)
    event_finish = Column(DateTime, nullable=True)
    event_user_id = Column(UUIDType(binary=False),
                           ForeignKey(User.id), nullable=True)
    color = Column(String(255), nullable=True)
    week_days = Column(String(255), nullable=False)

    instructor = relationship('Instructor', back_populates='schedule')
    student = relationship('Student', back_populates='schedule')
    event = relationship('SkillsSchedule', back_populates='event')
    specialty = relationship('Specialty', back_populates='schedule')
    payment = relationship('Payment', back_populates='schedule')
    billing = relationship('Billing', back_populates='schedule')
    skill_schedule = relationship('SkillsSchedule', back_populates='schedule')


class ProcedureSchedule(ModelBase):
    __tablename__ = 'procedures_schedueles'
    schedule_id = Column(UUIDType(binary=False),
                         ForeignKey(Schedule.id), nullable=False)
    student_id = Column(UUIDType(binary=False),
                        ForeignKey(Student.id), nullable=False)
    skill_id = Column(UUIDType(binary=False),
                      ForeignKey(Skill.id), nullable=False)
    procedure_id = Column(UUIDType(binary=False),
                          ForeignKey(Procedure.id), nullable=False)

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

    skills = relationship('Skill', back_populates='procedure')
    executions = relationship('Execution', back_populates='procedure')

    skill_name = association_proxy('skills', 'name')


class Execution(ModelBase):
    __tablename__ = 'executions'

    schedule_id = Column(UUIDType(binary=False),
                         ForeignKey(Schedule.id), nullable=False)
    procedure_id = Column(UUIDType(binary=False),
                          ForeignKey(Procedure.id), nullable=False)
    procedure_schedule_id = Column(UUIDType(binary=False),
                                   ForeignKey(ProcedureSchedule.id), nullable=False)

    trie = Column(Integer(), nullable=False)
    time = Column(String(255), nullable=False)
    success = Column(Boolean(), nullable=False)
    user_id = Column(UUIDType(binary=False),
                     ForeignKey(User.id), nullable=False)
    help_type = Column(Enum(HelpEnum), nullable=False)

    procedure = relationship('ProcedureSchedule', back_populates='executions')


class SkillsSchedule(ModelBase):
    __tablename__ = 'skills_schedules'

    schedule_id = Column(UUIDType(binary=False),
                         ForeignKey(Schedule.id), nullable=False)
    skill_id = Column(UUIDType(binary=False),
                      ForeignKey(Skill.id), nullable=False)
    finished = Column(Boolean, default=False, nullable=True)

    skills = relationship('Skill', back_populates='schedule')
    event = relationship('Schedule', back_populates='event')
    schedule = relationship('Schedule', back_populates='skill_schedule')

    skill_name = association_proxy('skills', 'name')
    event_id = association_proxy('event', 'event_id')


class Payment(ModelBase):
    __tablename__ = 'payments'

    company_id = Column(UUIDType(binary=False),
                        ForeignKey(Company.id), nullable=False)
    schedule_id = Column(UUIDType(binary=False),
                         ForeignKey(Schedule.id), nullable=False)
    instructor_id = Column(UUIDType(binary=False),
                           ForeignKey(Instructor.id), nullable=True)

    reference = Column(String(20), nullable=True)
    value = Column(Float(), nullable=True)
    date_due = Column(Date, nullable=False)
    date_scheduled = Column(Date, nullable=True)
    date_done = Column(Date, nullable=True)
    description = Column(String(250), nullable=True)
    status = Column(Enum(PaymentEnum), nullable=False)

    schedule = relationship('Schedule', back_populates='payment')
    instructor = relationship('Instructor', back_populates='payment')


class Billing(ModelBase):
    __tablename__ = 'bilings'

    company_id = Column(UUIDType(binary=False),
                        ForeignKey(Company.id), nullable=False)
    schedule_id = Column(UUIDType(binary=False),
                         ForeignKey(Schedule.id), nullable=False)
    student_id = Column(UUIDType(binary=False),
                        ForeignKey(Student.id), nullable=True)

    reference = Column(String(20), nullable=True)
    category = Column(Enum(CategoryEnum), nullable=True)
    value = Column(Float(), nullable=True)
    date_due = Column(Date, nullable=False)
    date_done = Column(Date, nullable=True)
    description = Column(String(250), nullable=True)
    status = Column(Enum(BillingEnum), nullable=False)
    generate_invoice = Column(Boolean, nullable=True)
    date_generate_invoice = Column(DateTime, nullable=True)

    schedule = relationship('Schedule', back_populates='billing')
    student = relationship('Student', back_populates='billing')
    invoice_billings = relationship('InvoiceBilling', back_populates='billing')


class CompanyInvoiceToken(ModelBase):
    __tablename__ = 'company_invoice_tokens'

    company_id = Column(UUIDType(binary=False),
                        ForeignKey(Company.id), nullable=False)
    token = Column(String(250), nullable=False)


class Invoice(ModelBase):
    __tablename__ = 'invoices'

    company_id = Column(UUIDType(binary=False),
                        ForeignKey(Company.id), nullable=False)

    reference = Column(String(250), nullable=False)
    api_status = Column(String(250), nullable=True)
    sender_status = Column(Enum(InvoiceSenderStatusEnum), nullable=False)

    invoice_billings = relationship('InvoiceBilling', back_populates='invoice')


class InvoiceBilling(ModelBase):
    __tablename__ = 'invoice_billings'

    invoice_id = Column(UUIDType(binary=False),
                        ForeignKey(Invoice.id), nullable=False)
    billing_id = Column(UUIDType(binary=False),
                        ForeignKey(Billing.id), nullable=False)

    invoice = relationship('Invoice', back_populates='invoice_billings')
    billing = relationship('Billing', back_populates='invoice_billings')


class InvoiceLog(ModelBase):
    __tablename__ = 'invoice_logs'

    invoice_id = Column(UUIDType(binary=False),
                        ForeignKey(Invoice.id), nullable=False)
    history = Column(String(250), nullable=False)


class HealthPlan(ModelBase):
    __tablename__ = 'health_plans'

    company_id = Column(UUIDType(binary=False),
                        ForeignKey(Company.id), nullable=False)

    social_name = Column(String(100), nullable=True)
    fantasy_name = Column(String(100), nullable=True)
    document = Column(String(20), nullable=True)
    address = Column(String(255), nullable=False)
    number = Column(Integer(), nullable=True)
    complement = Column(String(255), nullable=True)
    zip_code = Column(String(255), nullable=False)
    city = Column(String(255), nullable=False)
    district = Column(String(50), nullable=True)
    state = Column(String(255), nullable=False)
    country = Column(String(255), nullable=True)
    municipal_registration = Column(String(255), nullable=True)
    email = Column(String(50), nullable=False)
    phone = Column(String(50), nullable=True)
    active = Column(Boolean(), nullable=True)

    student_plan = relationship('StudentHealthPlan', back_populates='plan')


class StudentHealthPlan(ModelBase):
    __tablename__ = 'student_health_plans'

    student_id = Column(UUIDType(binary=False),
                        ForeignKey(Student.id), nullable=False)
    health_plan_id = Column(UUIDType(binary=False),
                            ForeignKey(HealthPlan.id), nullable=False)

    plan = relationship('HealthPlan', back_populates='student_plan')


class StudentDoctor(ModelBase):
    __tablename__ = 'student_doctors'

    student_id = Column(UUIDType(binary=False),
                        ForeignKey(Student.id), nullable=False)

    name = Column(String(100), nullable=True)
    email = Column(String(50), nullable=False)
    phone = Column(String(50), nullable=True)


class StudentMedicine(ModelBase):
    __tablename__ = 'student_medicines'

    student_id = Column(UUIDType(binary=False),
                        ForeignKey(Student.id), nullable=False)

    medicine = Column(String(100), nullable=True)
    amount = Column(String(50), nullable=False)
    measure = Column(String(50), nullable=True)
    schedules = Column(String(50), nullable=True)
    anotations = Column(String(250), nullable=True)


class OrderPayment(ModelBase):
    __tablename__ = 'order_payments'

    company_id = Column(UUIDType(binary=False),
                        ForeignKey(Company.id), nullable=False)
    instructor_id = Column(UUIDType(binary=False),
                        ForeignKey(Instructor.id), nullable=False)

    number = Column(String(20), nullable=False)
    period_reference = Column(String(20), nullable=False)
    description = Column(String(200), nullable=True)
    value = Column(Float(), nullable=False)
    date_due = Column(Date, nullable=False)
    date_done = Column(Date, nullable=True)
    status = Column(Enum(OrderPaymentEnum), nullable=False)


    instructor = relationship('Instructor', back_populates='order_payments')

class PaymentReference(ModelBase):
    __tablename__ = 'payment_references'

    order_payment_id = Column(UUIDType(binary=False),
                        ForeignKey(OrderPayment.id), nullable=False)
    payment_id = Column(UUIDType(binary=False),
                        ForeignKey(Payment.id), nullable=False)
