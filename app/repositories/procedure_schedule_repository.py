from typing import List
from uuid import UUID
from sqlalchemy.orm import Session
from app.schemas.procedure_schemas import ProcedureSchemaIn, ProcedureSchemaOut
from db.models import ProcedureSchedule


class ProcedureScheduleRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self,
               schedule_id: UUID,
               student_id: UUID,
               procedure_in: ProcedureSchemaOut) -> ProcedureSchemaOut:
        procedure_schedule = ProcedureSchedule(
            schedule_id=schedule_id,
            student_id=student_id,
            skill_id=procedure_in.skill_id,
            procedure_id=procedure_in.id,
            tries=procedure_in.tries,
            goal=procedure_in.goal,
            period=procedure_in.period,
            name=procedure_in.name,
            objective=procedure_in.objective,
            stimulus=procedure_in.stimulus,
            answer=procedure_in.answer,
            consequence=procedure_in.consequence,
            materials=procedure_in.materials,
            help=procedure_in.help,
        )

        self.session.add(procedure_schedule)
        self.session.commit()

        return procedure_schedule

    def get_id(self, id: UUID) -> ProcedureSchemaOut:
        return ProcedureSchedule.query(self.session).filter(ProcedureSchedule.id == id).first()

    def get_all(self,) -> List[ProcedureSchemaOut]:
        return ProcedureSchedule.query(self.session).all()

    def get_schedule_all(self, schedule_id: UUID,) -> List[ProcedureSchemaOut]:
        return ProcedureSchedule.query(self.session).filter(ProcedureSchedule.schedule_id == schedule_id).all()

    def get_schedule_student_skill(self, schedule_id: UUID, student_id: UUID, skill_id: UUID) -> List[ProcedureSchemaOut]:
        return ProcedureSchedule.query(self.session).filter(
            ProcedureSchedule.schedule_id == schedule_id,
            ProcedureSchedule.student_id == student_id,
            ProcedureSchedule.skill_id == skill_id,
        ).all()

    def get_student_procedure(self, student_id: UUID, procedure_id: UUID) -> List[ProcedureSchemaOut]:
        return ProcedureSchedule.query(self.session).filter(
            ProcedureSchedule.student_id == student_id,
            ProcedureSchedule.procedure_id == procedure_id,
        ).all()

    def get_schedule_skill(self, schedule_id: UUID, skill_id: UUID) -> List[ProcedureSchemaOut]:
        return ProcedureSchedule.query(self.session).filter(
            ProcedureSchedule.schedule_id == schedule_id,
            ProcedureSchedule.skill_id == skill_id,
        ).all()

    def update(self, procedure_schedule: ProcedureSchedule, procedure_in: ProcedureSchemaIn) -> ProcedureSchemaOut:
        procedure_schedule.tries = procedure_in.tries
        procedure_schedule.goal = procedure_in.goal
        procedure_schedule.period = procedure_in.period
        procedure_schedule.name = procedure_in.name.upper()
        procedure_schedule.objective = procedure_in.objective.upper()
        procedure_schedule.stimulus = procedure_in.stimulus.upper()
        procedure_schedule.answer = procedure_in.answer.upper()
        procedure_schedule.consequence = procedure_in.consequence.upper()
        procedure_schedule.materials = procedure_in.materials.upper()
        procedure_schedule.help = procedure_in.help.upper()

        self.session.add(procedure_schedule)
        self.session.commit()

        return procedure_schedule

    def delete(self, id: UUID) -> bool:
        procedure_schedule = ProcedureSchedule.query(
            self.session).filter(ProcedureSchedule.id == id).first()

        self.session.delete(procedure_schedule)
        self.session.commit()

        return True

    def check_procedure_schedule_student(self, schedule_id: UUID, student_id: UUID, procedure_id: UUID) -> ProcedureSchemaOut:
        return ProcedureSchedule.query(self.session).filter(
            ProcedureSchedule.schedule_id == schedule_id,
            ProcedureSchedule.student_id == student_id,
            ProcedureSchedule.procedure_id == procedure_id,
        ).first()

    def get_skill_procedures(self, skill_id: UUID, student_id: UUID) -> List[ProcedureSchemaOut]:
        query = ProcedureSchedule.query(self.session).filter(
            ProcedureSchedule.skill_id == skill_id,
        )

        if student_id:
            query = query.filter(ProcedureSchedule.student_id == student_id)

        return query.all()
    
    def get_distinct_skill_procedure(self, skill_id, schedule_id: UUID) -> List[ProcedureSchemaOut]:
        return ProcedureSchedule.query(self.session).filter(
            ProcedureSchedule.skill_id == skill_id,
             ProcedureSchedule.schedule_id == schedule_id,
        ).distinct(ProcedureSchedule.procedure_id).all()