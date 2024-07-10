from uuid import UUID
from db.models import ProcedureSchedule
from schemas.procedure_schemas import ProcedureIn
from sqlalchemy.orm import Session


class Objective:
    def __init__(self, session: Session):
        self.session = session
        
    def save(self, schedule_id: UUID, student_id: UUID, skill: UUID, procedure_in: ProcedureIn):
        procedure = ProcedureSchedule(
            schedule_id=schedule_id,
            student_id=student_id,
            skill_id=skill,
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
        self.session.add(procedure)
        self.session.flush()
        
        return procedure
        
    def delete(self, id: UUID):
        procedure = ProcedureSchedule.query(self.session).filter(
            ProcedureSchedule.id == id).first()
        
        self.session.add(procedure)
        self.session.commit()
        
        return True