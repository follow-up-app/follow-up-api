import unittest
from unittest.mock import Mock
from app.schemas.specialty_schemas import SpecialtySchemaIn
from app.services.specialty_service import SpecialtyService
from db.models import Specialty


class TestSpecialtyService(unittest.TestCase):
    def test_create(self):
        specialty_mock_repository = Mock()
        specialty_mock_repository.create.return_value = Specialty(
            id='54e67113-4300-4897-b0f4-2b279c6bd2f0',
            company_id='469264d5-6203-4f2e-aa2e-fdb0d939bc96',
            name='PHONO',
            description='Unit tests',
            value_hour=100.00
        )
        specialty_service = SpecialtyService(specialty_mock_repository)

        new_specialty = SpecialtySchemaIn(
            name='PHONO',
            description='Unit tests',
            value_hour=100.00
        )

        created_item = specialty_service.create(new_specialty)
        self.assertEqual(
            created_item.id, '54e67113-4300-4897-b0f4-2b279c6bd2f0')

    def test_update(self):
        specialty_mock_repository = Mock()
        specialty_mock_repository.update.return_value = Specialty(
            id='54e67113-4300-4897-b0f4-2b279c6bd2f0',
            company_id='469264d5-6203-4f2e-aa2e-fdb0d939bc96',
            name='PHONO',
            description='Unit tests',
            value_hour=150.00
        )

        specialty_mock_repository.id.return_value = Specialty(
            id='54e67113-4300-4897-b0f4-2b279c6bd2f0',
            company_id='469264d5-6203-4f2e-aa2e-fdb0d939bc96',
            name='PHONO',
            description='Unit tests',
            value_hour=100.00
        )

        new_specialty = SpecialtySchemaIn(
            name='PHONO',
            description='Unit tests',
            value_hour=150.00
        )
        specialty_service = SpecialtyService(specialty_mock_repository)
        created_item = specialty_service.update(
            id='54e67113-4300-4897-b0f4-2b279c6bd2f0', specialty_in=new_specialty)
        self.assertEqual(
            created_item.id, '54e67113-4300-4897-b0f4-2b279c6bd2f0')
        self.assertEqual(
            created_item.value_hour, 150.00)
