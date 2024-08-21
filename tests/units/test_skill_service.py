import unittest
from unittest.mock import Mock
from app.services.procedure_service import ProcedureService
from app.services.skill_service import SkillService
from db.models import Procedure, Skill


class TestSkillService(unittest.TestCase):
    def test_create(self):
        mock_repository = Mock()
        mock_repository.create.return_value = Skill(
            id='50820477-873f-45e4-8893-e6548fa141ca',
            company_id='469264d5-6203-4f2e-aa2e-fdb0d939bc96',
            name='Fight',
            objective='all fight'
        )

        mock_procedure_repositoty = Mock()
        mock_procedure_repositoty.create.return_value = Procedure(
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

        mock_procedure_service = ProcedureService(
            procedure_repository=mock_procedure_repositoty)
        skill_service = SkillService(
            skill_repository=mock_repository, procedure_service=mock_procedure_service)

        new_skill = Skill(
            company_id='469264d5-6203-4f2e-aa2e-fdb0d939bc96',
            name='Fight',
            objective='all fight'
        )

        created_item = skill_service.create(new_skill)
        self.assertEqual(
            created_item.id, '50820477-873f-45e4-8893-e6548fa141ca')
        self.assertEqual(created_item.name, 'Fight')

    def test_update(self):
        mock_repository = Mock()
        mock_exists_function = Mock(return_value=True)
        mock_repository.update.return_value = Skill(
            id='50820477-873f-45e4-8893-e6548fa141ca',
            company_id='469264d5-6203-4f2e-aa2e-fdb0d939bc96',
            name='Fight',
            objective='all fight'
        )
        mock_procedure_repositoty = Mock()
        mock_procedure_repositoty.create.return_value = Procedure(
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

        mock_procedure_service = ProcedureService(
            procedure_repository=mock_procedure_repositoty)
        skill_service = SkillService(
            skill_repository=mock_repository, procedure_service=mock_procedure_service)
        skill_service.skill_repository.get_id = mock_exists_function
        new_skill = Skill(
            company_id='469264d5-6203-4f2e-aa2e-fdb0d939bc96',
            name='Fight',
            objective='all fight'
        )
        created_item = skill_service.update(
            id='450820477-873f-45e4-8893-e6548fa141ca', skill_in=new_skill)
        self.assertEqual(
            created_item.id, '50820477-873f-45e4-8893-e6548fa141ca')

        mock_exists_function.return_value = False
        with self.assertRaises(ValueError):
            skill_service.update(
                id='450820477-873f-45e4-8893-e6548fa141ca', skill_in=new_skill)
