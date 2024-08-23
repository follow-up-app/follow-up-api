from typing import List
from uuid import UUID
from app.constants.enums.schedule_enum import ScheduleEnum
from app.constants.exceptions.execution_exceptions import ExecutionNotFoundError, ExecutionTriesError
from app.constants.exceptions.procedure_exceptions import ProcedureNotFoundError
from app.constants.exceptions.schedule_exceptions import ScheduleNotFoundError
from app.repositories.execution_repository import ExecutionRepository
from app.schemas.execution_schemas import ExecutionSchemaIn, ExecutionSchemaOut
from app.services.procedure_schedule_service import ProcedureScheduleService
from app.services.schedule_service import ScheduleService


class ExecutionService:
    def __init__(self, execution_repository: ExecutionRepository, schedule_service: ScheduleService, procedure_schedule_service: ProcedureScheduleService):
        self.execution_repository = execution_repository
        self.schedule_service = schedule_service
        self.procedure_schedule_service = procedure_schedule_service

    def create(self, execution_in: ExecutionSchemaIn) -> ExecutionSchemaOut:
        schedule = self.schedule_service.get_id(execution_in.schedule_id)
        if not schedule:
            raise ValueError(ScheduleNotFoundError.MESSAGE)
     
        procedure_schedule = self.procedure_schedule_service.get_id(
            execution_in.procedure_id)
        if not procedure_schedule:
            raise ValueError(ProcedureNotFoundError.MESSAGE)

        tries = self.execution_repository.count_for_procedure_in_schedule(
            procedure_schedule.procedure_id, schedule.id)

        if tries >= execution_in.trie or execution_in.trie > procedure_schedule.tries:
            raise ValueError(ExecutionTriesError.MESSAGE)

        if schedule.status == ScheduleEnum.SCHEDULED:
            self.schedule_service.in_progress(schedule)

        if schedule.student_arrival == None:
            self.schedule_service.student_arrival(schedule.id)

        return self.execution_repository.create(
            schedule.id,
            procedure_schedule.procedure_id,
            procedure_schedule.id, execution_in)

    def get_id(self, id: UUID) -> ExecutionSchemaOut:
        return self.execution_repository.get_id(id)

    def get_shedule_procedure(self, schedule_id: UUID, procedure_schedule_id: UUID) -> List[ExecutionSchemaOut]:
        return self.execution_repository.get_shedule_procedure(schedule_id, procedure_schedule_id)

    def get_schedule(self, schedule_id: UUID):
        return self.execution_repository.get_schedule(schedule_id)

    def count_execution_independent(self, schedule_id: UUID, procedure_id: UUID) -> int:
        return self.execution_repository.count_execution_independent(schedule_id, procedure_id)

    def count_for_procedure_in_schedule(self, procedure_schedule_id: UUID, schedule_id: UUID) -> int:
        return self.execution_repository.count_for_procedure_in_schedule(procedure_schedule_id, schedule_id)

    def update(self, id: UUID, execution_in: ExecutionSchemaIn) -> ExecutionSchemaOut:
        execution = self.execution_repository.get_id(id)
        if not execution:
            raise ValueError(ExecutionNotFoundError.MESSAGE)

        return self.execution_repository.update(execution, execution_in)

    def delete(self, id: UUID) -> bool:
        return self.execution_repository.delete(id)
