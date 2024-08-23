from datetime import datetime
from typing import List
from uuid import UUID
from app.constants.exceptions.schedule_exceptions import ScheduleNotFoundError
from app.constants.exceptions.skill_excepetions import SkillNotFoundError
from app.schemas.follow_up_schemas import FiltersSchemaIn, ScheduleSchemaFollowUp, ScheduleSchemaFollowUpMobile
from app.schemas.schedule_schemas import ScheduleSchemaOut
from app.services.execution_service import ExecutionService
from app.services.procedure_schedule_service import ProcedureScheduleService
from app.services.schedule_service import ScheduleService
from app.services.skill_schedule_service import SkillScheduleService
from app.services.skill_service import SkillService


class FollowUpService:
    def __init__(self,
                 schedule_service: ScheduleService,
                 skill_schedule_service: SkillScheduleService,
                 skill_service: SkillService,
                 procedure_schedule_service: ProcedureScheduleService,
                 execution_service: ExecutionService,
                 ):
        self.schedule_service = schedule_service
        self.skill_schedule_service = skill_schedule_service
        self.skill_service = skill_service
        self.procedure_schedule_service = procedure_schedule_service
        self.execution_service = execution_service

    def get_follow_up(self) -> List[ScheduleSchemaOut]:
        schedules = self.schedule_service.get_follow_up()
        for schedule in schedules:
            schedule.skills = self.skill_schedule_service.get_schedule(
                schedule.id)

        return schedules

    def get_follow_up_schedule(self, schedule_id: UUID) -> ScheduleSchemaFollowUp:
        schedule = self.schedule_service.get_id(schedule_id)
        if not schedule:
            raise ValueError(ScheduleNotFoundError.MESSAGE)

        skills = self.skill_schedule_service.get_schedule(schedule.id)

        for skill in skills:
            executions = []
            procedures = self.procedure_schedule_service.get_schedule_student_skill(
                schedule.id, schedule.student_id, skill.skill_id)
            

            for procedure in procedures:
                procedure.points = 0
                executions = self.execution_service.get_shedule_procedure(
                    schedule.id, procedure.id)

                if executions:
                    procedure.points = round(self.execution_service.count_execution_independent(
                        schedule.id, procedure.procedure_id) / procedure.tries * 100, 2)
                    procedure.executions = executions
                        
            skill.procedures = procedures

        schedule.skills = skills

        return schedule

    def mobile_schedule(self, schedule_id: UUID, skill_schedule_id: UUID) -> ScheduleSchemaFollowUpMobile:
        schedule = self.schedule_service.get_id(schedule_id)
        if not schedule:
            raise ValueError(ScheduleNotFoundError.MESSAGE)

        skill_schedule = self.skill_schedule_service.get_id(skill_schedule_id)

        skill = self.skill_service.get_id(skill_schedule.skill_id)
        if not skill:
            raise ValueError(SkillNotFoundError.MESSAGE)

        procedures = self.procedure_schedule_service.get_schedule_student_skill(
            schedule.id, schedule.student_id, skill.id)

        skill.procedures = procedures
        schedule.skill = skill

        for procedure in skill.procedures:
            executions = self.execution_service.count_for_procedure_in_schedule(
                procedure.id, schedule.id)
            
            procedure.total_exec = int(executions)
            procedure.data_chart = round(executions / procedure.tries, 2)
            procedure.app_active = True
            if executions >= procedure.tries:
                procedure.app_active = False

        others_skills = self.skill_schedule_service.get_schedule(schedule.id)

        outhers = []
        for skl in others_skills:
            prcs = self.procedure_schedule_service.get_schedule_student_skill(
                schedule.id, schedule.student_id, skl.skill_id)
            for p in prcs:
                excs = self.execution_service.count_for_procedure_in_schedule(
                   p.id, schedule.id)
                p.app_active = True
                if excs >= p.tries:
                    p.app_active = False
                outhers.append(p)

        schedule.outhers = outhers

        return schedule

    def get_filters(self, filters_in: FiltersSchemaIn) -> List[ScheduleSchemaFollowUp]:
        start = datetime.combine(filters_in.start, datetime.min.time())
        end = datetime.combine(filters_in.end, datetime.max.time())
        
        schedules = self.schedule_service.get_date_filter(start, end)
        
        for schedule in schedules:
            skills = self.skill_schedule_service.get_schedule(schedule.id)
            schedule.skills = skills
            
        return schedules
        
    def get_student(self, student_id: UUID) -> List[ScheduleSchemaFollowUp]:
        return self.schedule_service.get_student(student_id)
        