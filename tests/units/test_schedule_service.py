import unittest
from unittest.mock import Mock
from app.constants.enums.genere_enum import GenereEnum
from app.constants.enums.partenal_enum import PartenalEnum
from app.constants.enums.repeat_enum import RepeatEnum
from app.constants.enums.schedule_enum import ScheduleEnum
from app.constants.enums.status_enum import StatusEnum
from app.schemas.instructor_schema import InstructorSchemaOut
from app.schemas.procedure_schemas import ProcedureSchemaOut
from app.schemas.responsible_contract_schemas import ResponsibleContractSchemaOut
from app.schemas.schedule_schemas import ScheduleSchemaIn, ScheduleSchemaOut, SkillScheduleSchemaOut
from app.schemas.skill_schemas import SkillSchemaOut
from app.schemas.student_schemas import StudentSchemaOut
from app.services.address_contract_service import AddressContractService
from app.services.contractor_service import ContractorService
from app.services.instructor_service import InstructorService
from app.services.procedure_schedule_service import ProcedureScheduleService
from app.services.procedure_service import ProcedureService
from app.services.responsible_contract_service import ResponsibleContractService
from app.services.schedule_service import ScheduleService
from app.services.skill_schedule_service import SkillScheduleService
from app.services.skill_service import SkillService
from app.services.student_service import StudentService
from app.services.user_service import UserService


class TestScheduleService(unittest.TestCase):
    def test_create(self):
        mock_repository = Mock()
        mock_repository.create.return_value = ScheduleSchemaOut(
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

        student_mock_repository = Mock()
        student_mock_repository.get_id.return_value = StudentSchemaOut(
            id='18b941d7-6d85-4f84-a8fa-13b9f71d6806',
            contractor_id='ef83d3dd-d7fc-41dd-8cc2-4e69ef67b594',
            fullname='Anakin Skywalker',
            birthday='2015-12-01',
            allergy=None,
            genere=GenereEnum.MALE,
            document='101.202.301-10',
            indentity_number='20222',
            org_exp='SSJ',
            uf_exp='RS',
            nationality='Brasil',
            email=None,
            phone=None,
            avatar=None,
            informations=None,
            status=StatusEnum.ACTIVE
        )

        mock_contractor_repository = Mock()
        mock_reponsible_repository = Mock()
        mock_reponsible_repository.get_contractor_id.return_value = [ResponsibleContractSchemaOut(
            id='c54112e3-abf7-42e7-9b40-9fa3338c4adc',
            contractor_id='ef83d3dd-d7fc-41dd-8cc2-4e69ef67b594',
            fullname='Mother Anakin',
            birthday='1985-12-12',
            document='101.202.301-10',
            indentity_number='0001',
            org_exp=None,
            uf_exp=None,
            nationality=None,
            email=None,
            phone=None,
            bond=PartenalEnum.MOTHER,
        )]
        mock_address_repository = Mock()
        contractor_service = ContractorService(
            contractor_repository=mock_contractor_repository)
        responsible_contract_service = ResponsibleContractService(
            responsible_contract_repository=mock_reponsible_repository
        )
        address_contract_service = AddressContractService(
            address_contract_repository=mock_address_repository
        )

        student_service = StudentService(
            student_repository=student_mock_repository,
            contractor_service=contractor_service,
            responsible_contract_service=responsible_contract_service,
            address_contract_service=address_contract_service
        )

        instructor_mock_repository = Mock()
        instructor_mock_repository.get_id.return_value = InstructorSchemaOut(
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

        mock_user_repository = Mock()
        mock_email = Mock()
        mock_address_repository = Mock()
        user_service = UserService(
            user_repository=mock_user_repository, mailer=mock_email)

        instructor_payment_repository = Mock()

        instructor_service = InstructorService(
            instructor_repository=instructor_mock_repository,
            user_service=user_service,
            address_instructor_repository=mock_address_repository,
            instructor_payment_repository=instructor_payment_repository
        )

        skill_mock_repository = Mock()
        skill_mock_repository.create.return_value = [SkillSchemaOut(
            id='50820477-873f-45e4-8893-e6548fa141ca',
            name='Fight',
            objective='all fight'
        )]
        procedure_mock_repositoty = Mock()
        procedure_mock_repositoty.get_all.return_value = [ProcedureSchemaOut(
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
        )]
        procedure_service = ProcedureService(
            procedure_repository=procedure_mock_repositoty)

        skill_service = SkillService(
            skill_repository=mock_repository, procedure_service=procedure_service)

        skill_schedule_mock_repositoty = Mock()
        skill_schedule_mock_repositoty.create.return_value = SkillScheduleSchemaOut(
            id='61bc091d-58ad-4544-bd88-6572cc0d99d4',
            schedule_id='dbac77ac-95c4-4e61-8d51-7e77c39eb145',
            skill_id='50820477-873f-45e4-8893-e6548fa141ca',
            finished=False,
            skill_name='Fight'
        )
        skill_schedule_service = SkillScheduleService(
            skill_schedule_repository=skill_schedule_mock_repositoty
        )

        execution_mock_repositoty = Mock()

        procedure_schedule_repository = Mock()
        procedure_schedule_service = ProcedureScheduleService(
            procedure_schedule_repository)

        mock_exists_function = Mock(return_value=False)
        payment_mock = Mock()
        billing_mock = Mock()
        schedule_service = ScheduleService(
            schedule_repository=mock_repository,
            instructor_service=instructor_service,
            student_service=student_service,
            skill_service=skill_service,
            skill_schedule_service=skill_schedule_service,
            execution_repositoy=execution_mock_repositoty,
            procedure_schedule_service=procedure_schedule_service,
            procedure_service=procedure_service,
            payment_service=payment_mock,
            billing_service=billing_mock
        )
        schedule_service.check_instructor = mock_exists_function
        schedule_service.check_student = mock_exists_function

        new_schedule = ScheduleSchemaIn(
            specialty_id='54e67113-4300-4897-b0f4-2b279c6bd2f0',
            instructor_id='29241ac0-6a39-42d0-887b-6d5a3ec31df4',
            student_id='18b941d7-6d85-4f84-a8fa-13b9f71d6806',
            skill_id=[
                '50820477-873f-45e4-8893-e6548fa141ca'
            ],
            start_hour='10:00',
            end_hour='11:00',
            repeat=RepeatEnum.WEEK,
            period=2,
            schedule_in='2024-12-10',
            procedures=[ProcedureSchemaOut(
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
            )]
        )

        created_item = schedule_service.create(new_schedule)

        self.assertIsInstance(created_item, list)
