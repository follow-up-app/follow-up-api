import unittest
from unittest.mock import Mock
from app.constants.enums.company_enum import CompanyEnum
from db.models import Company
from app.services.company_service import CompanyService


class TestCompanyService(unittest.TestCase):
    def test_create(self):
        mock_repository = Mock()
        mock_exists_function = Mock(return_value=False)

        mock_repository.create.return_value = Company(
            id='469264d5-6203-4f2e-aa2e-fdb0d939bc96',
            name="Skynet SA",
            document="00.000.000/0001-00",
            address="Street X",
            number_address="25",
            complement=None,
            zip_code="99999-99",
            city="Florianópolis",
            state="SC",
            country="Brazil",
            email="contact@skynet.org",
            phone="55548984863711",
            status=CompanyEnum.ACTIVE)

        company_service = CompanyService(mock_repository)
        company_service.company_repository.get_document = mock_exists_function

        new_company = Company(
            name="Skynet SA",
            document="00.000.000/0002-00",
            address="Street X",
            number_address="25",
            complement=None,
            zip_code="99999-99",
            city="Florianópolis",
            state="SC",
            country="Brazil",
            email="contact@skynet.org",
            phone="55548984863711"
        )
        created_item = company_service.create(new_company)
        self.assertEqual(
            created_item.id, '469264d5-6203-4f2e-aa2e-fdb0d939bc96')
        self.assertEqual(created_item.name, 'Skynet SA')

        mock_exists_function.return_value = True
        with self.assertRaises(ValueError):
            company_service.create(new_company)

    def test_update(self):
        mock_repository = Mock()
        mock_exists_function = Mock(return_value=True)

        mock_repository.update.return_value = Company(
            id='469264d5-6203-4f2e-aa2e-fdb0d939bc96',
            name="Skynet SA",
            document="00.000.000/0001-00",
            address="Street X",
            number_address="25",
            complement=None,
            zip_code="99999-99",
            city="Florianópolis",
            state="SC",
            country="Brazil",
            email="contact@skynet.org",
            phone="55548984863711",
            status=CompanyEnum.IN_ANALYSIS)

        company_service = CompanyService(mock_repository)
        company_service.company_repository.get_id = mock_exists_function

        new_company = Company(
            name="Skynet SA",
            document="00.000.000/0002-00",
            address="Street X",
            number_address="25",
            complement=None,
            zip_code="99999-99",
            city="Florianópolis",
            state="SC",
            country="Brazil",
            email="contact@skynet.org",
            phone="55548984863711",
            status=CompanyEnum.IN_ANALYSIS
        )
        created_item = company_service.update(
            id='469264d5-6203-4f2e-aa2e-fdb0d939bc96', company_in=new_company)
        self.assertEqual(
            created_item.id, '469264d5-6203-4f2e-aa2e-fdb0d939bc96')

        mock_exists_function.return_value = False
        with self.assertRaises(ValueError):
            company_service.update(
                id='469264d5-6203-4f2e-aa2e-fdb0d939bc96', company_in=new_company)
