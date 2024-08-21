import unittest
from unittest.mock import Mock
from app.services.procedure_service import ProcedureService
from db.models import Procedure


class TestProcedureService(unittest.TestCase):
    def test_create(self):
        mock_repository = Mock()
        mock_repository.create.return_value = Procedure(
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
        procedure_service = ProcedureService(
            procedure_repository=mock_repository)

        new_procedure = Procedure(
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

        created_item = procedure_service.create(
            skill_id='50820477-873f-45e4-8893-e6548fa141ca', procedure_in=new_procedure)
        self.assertEqual(
            created_item.id, 'b71335c6-c5e2-423c-8105-19e309d0f6a7')
        self.assertEqual(created_item.name, 'Boxe')

    def test_update(self):
        mock_repository = Mock()
        mock_exists_function = Mock(return_value=True)
        mock_repository.update.return_value = Procedure(
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
        procedure_service = ProcedureService(
            procedure_repository=mock_repository)

        new_procedure = Procedure(
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
        
        procedure_service.procedure_repository.get_id = mock_exists_function

        created_item = procedure_service.update(
            id='b71335c6-c5e2-423c-8105-19e309d0f6a7', procedure_in=new_procedure)
        self.assertEqual(
            created_item.id, 'b71335c6-c5e2-423c-8105-19e309d0f6a7')

        mock_exists_function.return_value = False
        with self.assertRaises(ValueError):
            procedure_service.update(
                id='b71335c6-c5e2-423c-8105-19e309d0f6a7', procedure_in=new_procedure)
