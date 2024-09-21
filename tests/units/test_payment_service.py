import unittest
from unittest.mock import Mock
from app.constants.enums.payment_enum import PaymentEnum
from app.constants.enums.repeat_enum import RepeatEnum
from app.constants.enums.schedule_enum import ScheduleEnum
from app.constants.enums.status_enum import StatusEnum
from app.schemas.instructor_schema import InstructorSchemaOut
from app.schemas.payment_schemas import PaymentSchemaIn
from app.schemas.schedule_schemas import ScheduleSchemaOut
from app.schemas.specialty_schemas import SpecialtySchemaOut
from app.services.payment_service import PaymentService
from db.models import Payment


class TestPaymentService(unittest.TestCase):
    def test_create(self):
        payment_mock_repository = Mock()
        payment_mock_repository.create.return_value = Payment(
            id='f888aa0e-24b5-4465-bc99-376e975fbad3',
            company_id='469264d5-6203-4f2e-aa2e-fdb0d939bc96',
            schedule_id='dbac77ac-95c4-4e61-8d51-7e77c39eb145',
            instructor_id='29241ac0-6a39-42d0-887b-6d5a3ec31df4',
            value=100.00,
            date_due='2024-12-10',
            date_scheduled=None,
            date_done=None,
            description=None,
            status=PaymentEnum.OPEN,
            updated_at='2024-12-10 10:00',
            created_date='2024-12-10 10:00'
        )

        payment_service = PaymentService(
            payment_mock_repository
        )

        schedule = ScheduleSchemaOut(
            id='dbac77ac-95c4-4e61-8d51-7e77c39eb145',
            company_id='469264d5-6203-4f2e-aa2e-fdb0d939bc96',
            specialty_id='54e67113-4300-4897-b0f4-2b279c6bd2f0',
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

        instructor = InstructorSchemaOut(
            id='29241ac0-6a39-42d0-887b-6d5a3ec31df4',
            company_id='469264d5-6203-4f2e-aa2e-fdb0d939bc96',
            fullname='Obi Wan knobe',
            birthday='1970-10-21',
            document='101.202.301-10',
            indentity_number='20222',
            org_exp='SSJ',
            uf_exp='RS',
            nationality='Brasil',
            document_company='0000',
            social_name='Jedi S.A.',
            fantasy_name='Jedi',
            email='obi.wan@jedi.com',
            phone='48984863711',
            whats_app=True,
            status=StatusEnum.ACTIVE
        )

        created_item = payment_service.create(
            schedule, instructor)
        self.assertEqual(
            created_item.id, 'f888aa0e-24b5-4465-bc99-376e975fbad3')

    def test_update(self):
        payment_mock_repository = Mock()
        payment_mock_repository.update.return_value = Payment(
            id='f888aa0e-24b5-4465-bc99-376e975fbad3',
            company_id='469264d5-6203-4f2e-aa2e-fdb0d939bc96',
            schedule_id='dbac77ac-95c4-4e61-8d51-7e77c39eb145',
            instructor_id='29241ac0-6a39-42d0-887b-6d5a3ec31df4',
            value=150.00,
            date_due='2024-12-10',
            date_scheduled=None,
            date_done=None,
            description=None,
            status=PaymentEnum.OPEN,
            updated_at='2024-12-10 10:00',
            created_date='2024-12-10 10:00'
        )

        payment_mock_repository.get_id.return_value = Payment(
            id='f888aa0e-24b5-4465-bc99-376e975fbad3',
            company_id='469264d5-6203-4f2e-aa2e-fdb0d939bc96',
            schedule_id='dbac77ac-95c4-4e61-8d51-7e77c39eb145',
            instructor_id='29241ac0-6a39-42d0-887b-6d5a3ec31df4',
            value=100.00,
            date_due='2024-12-10',
            date_scheduled=None,
            date_done=None,
            description=None,
            status=PaymentEnum.OPEN,
            updated_at='2024-12-10 10:00',
            created_date='2024-12-10 10:00'
        )

        payment_service = PaymentService(
            payment_mock_repository,
        )

        new_payment = PaymentSchemaIn(
            schedule_id='dbac77ac-95c4-4e61-8d51-7e77c39eb145',
            instructor_id='29241ac0-6a39-42d0-887b-6d5a3ec31df4',
            value=150.00,
            date_due='2024-12-10',
        )
        created_item = payment_service.update(
            id='f888aa0e-24b5-4465-bc99-376e975fbad3', payment_in=new_payment)
        self.assertEqual(
            created_item.id, 'f888aa0e-24b5-4465-bc99-376e975fbad3')
        self.assertEqual(
            created_item.value, 150.00)

        payment_mock_repository.get_id.return_value = None
        with self.assertRaises(ValueError):
            payment_service.update(
                id='f888aa0e-24b5-4465-bc99-376e975fbad3', payment_in=new_payment)
