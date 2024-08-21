from typing import List
from uuid import UUID
from sqlalchemy.orm import Session
from app.constants.enums.help_enum import HelpEnum
from app.schemas.execution_schemas import ExecutionSchemaIn, ExecutionSchemaOut
from db.models import Execution, User


class ExecutionRepository:
    def __init__(self, session: Session, current_user: User):
        self.session = session
        self.current_user = current_user

    def create(self, schedule_id: UUID, procedure_id: UUID, procedure_schedule: UUID, execution_in: ExecutionSchemaIn) -> ExecutionSchemaOut:
        execution = Execution(
            schedule_id=schedule_id,
            procedure_id=procedure_id,
            procedure_schedule_id=procedure_schedule,
            trie=execution_in.trie,
            time=execution_in.time,
            help_type=execution_in.help_type,
            user_id=self.current_user.id,
            success=True,
        )

        self.session.add(execution)
        self.session.commit()

        return execution

    def get_id(self, id: UUID) -> ExecutionSchemaOut:
        return Execution.query(self.session).filter(Execution.id == id).first()

    def get_shedule_procedure(self, schedule_id: UUID, procedure_id: UUID) -> List[ExecutionSchemaOut]:
        return Execution.query(self.session).filter(
            Execution.schedule_id == schedule_id,
            Execution.procedure_id == procedure_id).order_by(Execution.trie).all()

    def get_schedule(self, schedule_id: UUID) -> List[ExecutionSchemaOut]:
        return Execution.query(self.session).filter(Execution.schedule_id == schedule_id).all()

    def count_execution_independent(self, schedule_id: UUID, procedure_id: UUID) -> int:
        return Execution.query(self.session).filter(
            Execution.procedure_id == procedure_id,
            Execution.schedule_id == schedule_id,
            Execution.help_type == HelpEnum.INDEPENDENT).count()

    def count_for_procedure_in_schedule(self, procedure_schedule_id: UUID, schedule_id: UUID) -> int:
        return Execution.query(self.session).filter(Execution.procedure_schedule_id == procedure_schedule_id, Execution.schedule_id == schedule_id).count()

    def update(self, execution: Execution, execution_in: ExecutionSchemaIn) -> ExecutionSchemaOut:
        execution.time = execution_in.time
        execution.help_type = execution_in.help_type
        
        self.session.add(execution)
        self.session.commit()

        return execution

    def delete(self, id: UUID) -> bool:
        execution = Execution.query(self.session).filter(
            Execution.id == id).first()

        self.session.delete(execution)
        self.session.commit()

        return True
