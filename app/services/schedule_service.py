from typing import List, Tuple
from app.constants.enums.repeat_enum import RepeatEnum
from app.constants.enums.schedule_enum import ScheduleEnum
from app.constants.exceptions.instructor_exceptions import InstructorNotFoundError
from app.constants.exceptions.procedure_exceptions import ProcedureNotFoundError
from app.constants.exceptions.schedule_exceptions import InstructorNotAvailableError, ScheduleHourError, ScheduleNotFoundError, ScheduleNotRemoveError, StudentNotAvailableError
from app.constants.exceptions.student_exceptions import StudentNotFoundError
from app.repositories.execution_repository import ExecutionRepository
from app.repositories.schedule_repository import ScheduleRepository
from app.schemas.instructor_schema import InstructorSchemaOut
from app.schemas.procedure_schemas import ProcedureSchemaIn, ProcedureSchemaOut
from app.schemas.schedule_schemas import ScheduleSchemaIn, ScheduleSchemaOut, ScheduleUpadateSchamaIn, SlotDates, EventSlotOut
from app.schemas.student_schemas import StudentSchemaOut
from app.services.instructor_service import InstructorService
from app.services.payment_service import PaymentService
from app.services.procedure_schedule_service import ProcedureScheduleService
from app.services.procedure_service import ProcedureService
from app.services.skill_schedule_service import SkillScheduleService
from app.services.skill_service import SkillService
from app.services.student_service import StudentService
from datetime import date, datetime, timedelta
from uuid import UUID
from app.services.billing_service import BillingService
from app.repositories.invoice_repository import InvoiceRepository



class ScheduleService:
    def __init__(self,
                 schedule_repository: ScheduleRepository,
                 student_service: StudentService,
                 instructor_service: InstructorService,
                 skill_service: SkillService,
                 skill_schedule_service: SkillScheduleService,
                 execution_repositoy: ExecutionRepository,
                 procedure_service: ProcedureService,
                 procedure_schedule_service: ProcedureScheduleService,
                 payment_service: PaymentService,
                 billing_service: BillingService,
                 invoice_repository: InvoiceRepository
                 ):
        self.schedule_repository = schedule_repository
        self.student_service = student_service
        self.instructor_service = instructor_service
        self.skill_service = skill_service
        self.skill_schedule_service = skill_schedule_service
        self.execution_repositoy = execution_repositoy
        self.procedure_service = procedure_service
        self.procedure_schedule_service = procedure_schedule_service
        self.payment_service = payment_service
        self.billing_service = billing_service
        self.invoice_repository = invoice_repository

    def prepare(self, schedule_in: ScheduleSchemaIn) -> List[ScheduleSchemaOut]:
        event = self.schedule_repository.create_event(schedule_in)
        for slot in schedule_in.date_slots:
             for date in slot.dates:
                for hours in slot.time_slots:
                    schedule = self.create(schedule_in, date, event.id, hours.start_hour, hours.end_hour, slot)

        return schedule

    def create(self, schedule_in: ScheduleSchemaIn, data_schedule: date, event_id: UUID, start: str, end: str, slot: SlotDates) -> List[ScheduleSchemaOut]:
        days = schedule_in.period * 30
        max_date = data_schedule + timedelta(days=round(days))
        week_days = ",".join(str(item.value) for item in slot.date_weeks)

        period_ = max_date - data_schedule
        events = []

        instructor = self.instructor_service.get_id(slot.instructor_id)
        if not instructor:
            raise ValueError(InstructorNotFoundError.MESSAGE)

        student = self.student_service.get_id(schedule_in.student_id)
        if not student:
            raise ValueError(StudentNotFoundError.MESSAGE)

        period = schedule_in.period
        repeat = 30

        if schedule_in.repeat == RepeatEnum.WEEK:
            period = round(period_.days / 7)
            repeat = 7

        for _ in range(period):
            dates = self.dates_allowed(data_schedule, start, end, student.id, instructor.id)

            schedule = self.schedule_repository.create(
                    event_id,
                    student,
                    slot.specialty_id,
                    instructor,
                    dates[0],
                    dates[1],
                    schedule_in,
                    start,
                    end,
                    week_days)

            events.append(schedule)
            data_schedule += timedelta(days=repeat)

        for sch in events:
            for procedure in slot.procedures:
                self.procedure_schedule_service.create(
                    sch.id, student.id, procedure)
            self.skill_schedule_service.create(sch.id, slot.skill_id)

            self.payment_service.create(sch, instructor)
            self.billing_service.create(sch, student)

        return events

    def dates_allowed(self, date: date, start: str, end: str, student_id: UUID, instructor_id: UUID) -> Tuple[datetime, datetime]:
        date_i = f'{date} {start}'
        date_schedule_in = datetime.strptime(date_i, '%Y-%m-%d %H:%M')

        date_o = f'{date} {end}'
        date_schedule_out = datetime.strptime(date_o, '%Y-%m-%d %H:%M')

        if date_schedule_out <= date_schedule_in:
            raise ValueError(ScheduleHourError.MESSAGE)

        if self.check_instructor(instructor_id, date_schedule_in, date_schedule_out):
            raise ValueError(InstructorNotAvailableError.MESSAGE)

        if self.check_student(student_id, date_schedule_in, date_schedule_out):
            raise ValueError(StudentNotAvailableError.MESSAGE)

        return date_schedule_in, date_schedule_out

    def check_instructor(self, instructor_id: UUID, date_schedule_in: datetime, date_schedule_out: datetime) -> ScheduleSchemaOut:
        return self.schedule_repository.check_instructor(instructor_id, date_schedule_in, date_schedule_out)

    def check_student(self, student_id: UUID, date_schedule_in: datetime, date_schedule_out: datetime) -> ScheduleSchemaOut:
        return self.schedule_repository.check_student(student_id, date_schedule_in, date_schedule_out)

    def get_all(self) -> List[ScheduleSchemaOut]:
        return self.schedule_repository.get_all()

    def get_schedule(self) -> List[ScheduleSchemaOut]:
        schedules = self.schedule_repository.get_scheduled()
        for schedule in schedules:
            schedule.skills = self.skill_schedule_service.get_schedule(
                schedule.id)

        return schedules

    def get_id(self, id: UUID) -> ScheduleSchemaOut:
        schedule = self.schedule_repository.get_id(id)
        if not schedule:
            raise ValueError(ScheduleNotFoundError.MESSAGE)
        schedule.skills = self.skill_schedule_service.get_schedule(schedule.id)

        return schedule

    def get_instructor(self, instructor_id: UUID) -> InstructorSchemaOut:
        return self.schedule_repository.get_instructor(instructor_id)

    def get_instuctor_all(self, instructor_id: UUID) -> StudentSchemaOut:
        return self.schedule_repository.get_instuctor_all(instructor_id)

    def delete_many(self, event_id: UUID) -> bool:
        schedules = self.schedule_repository.get_event_future(event_id)
        if not schedules:
            raise ValueError('Não existem agendas futuras para este evento.')

        for schedule in schedules:
            self.process_delete(schedule.id)

        return True

    def process_delete(self, id: UUID) -> bool:
        billing = self.billing_service.get_by_schedule_id(id)
        invoice = self.invoice_repository.get_invoice_for_billing(billing.id)
        if invoice:
            raise ValueError(f"Já existe uma NFSe emitida para esta agenda. Faça o cancelamento antes de processeguir: Ref {invoice.invoice.reference}")

        executions = self.execution_repositoy.get_schedule(id)
        if executions:
            raise ValueError(ScheduleNotRemoveError.MESSAGE)

        skills = self.skill_schedule_service.get_schedule(id)
        procedures = self.procedure_schedule_service.get_schedule_all(id)

        for procedure in procedures:
            self.procedure_schedule_service.delete(procedure.id)

        for skill in skills:
            self.skill_schedule_service.delete(skill.id)

        self.payment_service.delete_for_schedule(id)
        self.billing_service.delete_for_schedule(id)
        self.schedule_repository.delete(id)

        return True


    def update(self, id: UUID, schedule_in: ScheduleUpadateSchamaIn) -> ScheduleSchemaOut:
        schedule = self.schedule_repository.get_id(id)
        if not schedule:
            raise ValueError(ScheduleNotFoundError.MESSAGE)

        if schedule_in.status == ScheduleEnum.IN_PROGRESS:
            return self.schedule_repository.in_progress(schedule)

        if schedule_in.status == ScheduleEnum.DONE:
            self.payment_service.update_status_schedule(schedule.id)
            self.billing_service.update_status_schedule(schedule.id)

            return self.schedule_repository.done(schedule)

    def student_arrival(self, id: UUID) -> ScheduleSchemaOut:
        schedule = self.schedule_repository.get_id(id)
        if not schedule:
            raise ValueError(ScheduleNotFoundError.MESSAGE)

        return self.schedule_repository.student_arrival(schedule)

    def get_avalible_instructor(self):
        instructor = self.instructor_service.get_instructor_user()
        if not instructor:
            raise ValueError(InstructorNotFoundError.MESSAGE)

        stmt = self.schedule_repository.get_avalible_instructor(instructor.id)
        response = {}
        for item in stmt:
            schedules = self.schedule_repository.get_schedule_instructor(
                instructor.id, item[0])
            response[item[0]] = []

            for schd in schedules:
                skills = self.skill_schedule_service.get_schedule(schd.id)

                for skill in skills:
                    lst = {
                        'id': schd.id,
                        'skill_schedule_id': skill.id,
                        'skill_name': skill.skill_name,
                        'day': schd.start.day,
                        'hour_start': schd.start.hour,
                        'min_start': schd.start.minute,
                        'hour_end': schd.end.hour,
                        'min_end': schd.end.minute,
                        'student': schd.student.id,
                        'name': schd.student.fullname,
                        'avatar': schd.student.avatar,
                        'height': 80,
                    }
                    response[item[0]].append(lst)

        return response

    def in_progress(self, schedule: ScheduleSchemaOut) -> ScheduleSchemaOut:
        return self.schedule_repository.in_progress(schedule)

    def get_today(self) -> List[ScheduleSchemaOut]:
        today = date.today()
        start_of_day = datetime.combine(today, datetime.min.time())
        end_of_day = datetime.combine(today, datetime.max.time())

        return self.schedule_repository.get_today(start_of_day, end_of_day)

    def get_student(self, student_id: UUID) -> ScheduleSchemaOut:
        schedule = self.schedule_repository.get_student(student_id)
        if not schedule:
            raise ValueError(ScheduleNotFoundError.MESSAGE)

        return schedule

    def get_procedures(self, id: UUID, skill_id: UUID) -> List[ProcedureSchemaOut]:
        schedule = self.schedule_repository.get_id(id)
        if not schedule:
            raise ValueError(ScheduleNotFoundError.MESSAGE)

        return self.procedure_schedule_service.get_schedule_skill(schedule.id, skill_id)

    def get_follow_up(self) -> List[ScheduleSchemaOut]:
        return self.schedule_repository.get_follow_up()

    def get_date_filter(self, start: datetime, end: datetime,  student_id: UUID) -> List[ScheduleSchemaOut]:
        return self.schedule_repository.get_date_filter(start, end, student_id)

    def get_event_id(self, event_id: UUID) -> EventSlotOut:
        event = self.schedule_repository.get_event_id(event_id)
        if not event:
            raise ValueError(ScheduleNotFoundError.MESSAGE)
        skills_schedule =  self.skill_schedule_service.all_skill_schedules_for_event(event.id)

        slots = []

        for sk_c in skills_schedule:
            slot = {
                'skill_id': sk_c.skill_id,
                'specialty_id': sk_c.schedule.specialty_id,
                'instructor_id': sk_c.schedule.instructor_id,
                'procedures': self.procedure_schedule_service.get_distinct_skill_procedure(sk_c.skill_id, sk_c.schedule_id),
                'all_procedures': self.procedure_service.get_all(sk_c.skill_id),
                'date_weeks': sk_c.schedule.week_days,
                'skills': self.skill_service.get_speciality(sk_c.schedule.specialty_id),
                'time_slots': []
            }
            hours_schedule =  self.schedule_repository.get_distinct_start_end_schedule(event_id, sk_c.skill_id, sk_c.schedule.week_days)

            for hr in hours_schedule:
                slot_time = {
                    'start_hour': hr.start_hour,
                    'end_hour': hr.end_hour
                }
                slot['time_slots'].append(slot_time)

            slots.append(slot)
        event.slots = slots

        return event

    def update_event(self, event_id: UUID, schedule_in: ScheduleSchemaIn) -> List[ScheduleSchemaOut]:
        event = self.schedule_repository.get_event_id(event_id)
        if not event:
            raise ValueError(ScheduleNotFoundError.MESSAGE)
        schedules = self.schedule_repository.get_event_future(event_id)
        for schedule in schedules:
            self.process_delete(schedule.id)

        return self.prepare(schedule_in)