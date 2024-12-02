from typing import List
from uuid import UUID
from sqlalchemy.orm import Session
from app.schemas.procedure_schemas import ProcedureSchemaIn, ProcedureSchemaOut
from db.models import Procedure


class ProcedureRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, skill_id: UUID, procedure_in: ProcedureSchemaIn) -> ProcedureSchemaOut:
        procedure = Procedure(
            skill_id=skill_id,
            tries=procedure_in.tries,
            goal=procedure_in.goal,
            period=procedure_in.period,
            name=procedure_in.name.upper(),
            objective=procedure_in.objective.upper(),
            stimulus=procedure_in.stimulus.upper(),
            answer=procedure_in.answer.upper(),
            consequence=procedure_in.consequence.upper(),
            materials=procedure_in.materials.upper(),
            help=procedure_in.help.upper(),
        )

        self.session.add(procedure)
        self.session.commit()

        return procedure

    def get_id(self, id: UUID) -> ProcedureSchemaOut:
        return Procedure.query(self.session).filter(Procedure.id == id).first()

    def get_all(self, skill_id: UUID) -> List[ProcedureSchemaOut]:
        return Procedure.query(self.session).filter(Procedure.skill_id == skill_id).all()

    def get_for_many_skills(self, skills: List[UUID]) -> List[ProcedureSchemaOut]:
        return Procedure.query(self.session).filter(Procedure.skill_id.in_(skills)).all()

    def update(self, procedure: Procedure, procedure_in: ProcedureSchemaIn) -> ProcedureSchemaOut:
        procedure.tries = procedure_in.tries
        procedure.goal = procedure_in.goal
        procedure.period = procedure_in.period
        procedure.name = procedure_in.name.upper()
        procedure.objective = procedure_in.objective.upper()
        procedure.stimulus = procedure_in.stimulus.upper()
        procedure.answer = procedure_in.answer.upper()
        procedure.consequence = procedure_in.consequence.upper()
        procedure.materials = procedure_in.materials.upper()
        procedure.help = procedure_in.help.upper()

        self.session.add(procedure)
        self.session.commit()

        return procedure
