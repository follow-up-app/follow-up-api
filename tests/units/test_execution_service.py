import unittest
from unittest.mock import Mock
from app.constants.enums.help_enum import HelpEnum
from app.constants.enums.repeat_enum import RepeatEnum
from app.constants.enums.schedule_enum import ScheduleEnum
from app.schemas.execution_schemas import ExecutionSchemaIn
from app.schemas.procedure_schemas import ProcedureSchemaOut
from app.schemas.schedule_schemas import ScheduleSchemaOut
from app.services.execution_service import ExecutionService
from app.services.procedure_schedule_service import ProcedureScheduleService
from app.services.schedule_service import ScheduleService
from db.models import Execution


class TestExecutionService(unittest.TestCase):
    def test_create(self):
        mock_repository = Mock()
        mock_repository.create.return_value = Execution(
            id='09f46eb1-883c-427a-8c71-18ab2bfd9b94',
            schedule_id='dbac77ac-95c4-4e61-8d51-7e77c39eb145',
            procedure_id='b71335c6-c5e2-423c-8105-19e309d0f6a7',
            procedure_schedule_id='9f902cc2-62b9-4d40-879a-a34a0c2e6970',
            trie=2,
            time='00:20:00',
            help_type=HelpEnum.INDEPENDENT,
            success=True,
            user_id='18b941d7-6d85-4f84-a8fa-13b9f71d6806',
            created_date='2024-12-10 10:00'
        )
        mock_repository.count_for_procedure_in_schedule.return_value = 1
        schedule_repository = Mock()
        schedule_repository.get_id.return_value = ScheduleSchemaOut(
            id='dbac77ac-95c4-4e61-8d51-7e77c39eb145',
            company_id='469264d5-6203-4f2e-aa2e-fdb0d939bc96',
            instructor_id='29241ac0-6a39-42d0-887b-6d5a3ec31df4',
            student_id='18b941d7-6d85-4f84-a8fa-13b9f71d6806',
            event_id='add7dae3-daa9-4dc2-8aca-aae756204ab8',
            title='Event Test',
            start='2024-12-10 10:00',
            end='2024-12-10 11:00',
            start_hour='10:00',
            end_hour='11:00',
            repeat=RepeatEnum.WEEK,
            period=2,
            status=ScheduleEnum.SCHEDULED,
            details=None,
            student_arrival=None,
            event_begin=None,
            event_finish=None,
            event_user_id=None,
            created_date='2024-12-10 10:00',
            updated_at='2024-12-10 10:00'
        )

        procedure_schedule_repository = Mock()
        procedure_schedule_repository.get_id.return_value = ProcedureSchemaOut(
            id='b71335c6-c5e2-423c-8105-19e309d0f6a7',
            skill_id='50820477-873f-45e4-8893-e6548fa141ca',
            tries=3,
            goal=0.8,
            period='3',
            name='Boxe',
            objective='fighters',
            stimulus=None,
            answer=None,
            consequence=None,
            materials=None,
            help=None,
            student_id=None
        )
        procedure_schedule_service = ProcedureScheduleService(
            procedure_schedule_repository=procedure_schedule_repository
        )

        schedule_service = ScheduleService(
            schedule_repository=schedule_repository,
            student_service=Mock(),
            instructor_service=Mock(),
            skill_service=Mock(),
            skill_schedule_service=Mock(),
            execution_repositoy=mock_repository,
            procedure_service=Mock(),
            procedure_schedule_service=procedure_schedule_service
        )

        execution_service = ExecutionService(
            execution_repository=mock_repository,
            schedule_service=schedule_service,
            procedure_schedule_service=procedure_schedule_service
        )

        new_execution = ExecutionSchemaIn(
            schedule_id='dbac77ac-95c4-4e61-8d51-7e77c39eb145',
            procedure_id='9f902cc2-62b9-4d40-879a-a34a0c2e6970',
            trie=2,
            time='00:20:00',
            help_type=HelpEnum.INDEPENDENT
        )
        created_item = execution_service.create(new_execution)
        self.assertEqual(
            created_item.id, '09f46eb1-883c-427a-8c71-18ab2bfd9b94')
