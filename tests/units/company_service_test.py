import unittest
from unittest.mock import Mock
from app.constants.enums.company_enum import CompanyEnum
from app.services.company_service import CompanyService
from app.schemas.company_schemas import CompanySchemaOut, CompanySchemaIn
import uuid


class CompanyServiceTest(unittest.TestCase):
    def test_create_success(self):
        mock_repository = Mock()
        mock_repository.create.return_value = CompanySchemaOut(
            id='469264d5-6203-4f2e-aa2e-fdb0d939bc96',
            fantasy_name="Skynet",
            social_name="Skynet SA",
            document="00.000.000/0001-00",
            address="Street X",
            number_address="25",
            complement=None,
            zip_code="99999-99",
            district="Ingleses",
            city="Florianópolis",
            state="SC",
            email="contact@skynet.org",
            phone="55548984863711",
            city_code='0001',
            aliquot=10,
            municipal_registration='000093',
            iss_retained=False,
            licences_n=50,
            api_nfes_token='AAIII',
            status=CompanyEnum.ACTIVE)

        company_service = CompanyService(mock_repository)
        company_service.company_repository.get_document = Mock(return_value=False)

        new_company = CompanySchemaIn(
            fantasy_name="Skynet",
            social_name="Skynet SA",
            document="00.000.000/0001-00",
            address="Street X",
            number_address="25",
            complement=None,
            zip_code="99999-99",
            district="Ingleses",
            city="Florianópolis",
            state="SC",
            email="contact@skynet.org",
            phone="55548984863711",
            city_code='0001',
            aliquot=10,
            municipal_registration='000093',
            iss_retained=False,
            licences_n=50,
            api_nfes_token='AAIII',
        )
        created_item = company_service.create(new_company)

        self.assertEqual(created_item.id, uuid.UUID('469264d5-6203-4f2e-aa2e-fdb0d939bc96'))
        self.assertEqual(created_item.fantasy_name, 'Skynet')
        self.assertEqual(created_item.social_name, 'Skynet SA')
        self.assertEqual(created_item.document, '00.000.000/0001-00')
        self.assertEqual(created_item.email, 'contact@skynet.org')
        self.assertEqual(created_item.licences_n, 50)
        self.assertEqual(created_item.status, CompanyEnum.ACTIVE)


    def test_does_not_create_existing_document(self):
        new_company = CompanySchemaIn(
            fantasy_name="Skynet",
            social_name="Skynet SA",
            document="00.000.000/0001-00",
            address="Street X",
            number_address="25",
            complement=None,
            zip_code="99999-99",
            district="Ingleses",
            city="Florianópolis",
            state="SC",
            email="contact@skynet.org",
            phone="55548984863711",
            city_code='0001',
            aliquot=10,
            municipal_registration='000093',
            iss_retained=False,
            licences_n=50,
            api_nfes_token='AAIII',
        )

        mock_repository = Mock()
        company_service = CompanyService(mock_repository)
        company_service.company_repository.get_document = Mock(return_value=True)
        with self.assertRaises(ValueError):
            company_service.create(new_company)


    def test_update_success(self):
        mock_repository = Mock()
        mock_repository.update.return_value = CompanySchemaOut(
            id='469264d5-6203-4f2e-aa2e-fdb0d939bc96',
            fantasy_name="Skynet",
            social_name="Skynet SA",
            document="00.000.000/0001-00",
            address="Street X",
            number_address="25",
            complement=None,
            zip_code="99999-99",
            district="Ingleses",
            city="Florianópolis",
            state="SC",
            email="contact@skynet.org",
            phone="55548984863711",
            city_code='0001',
            aliquot=10,
            municipal_registration='000093',
            iss_retained=False,
            licences_n=50,
            api_nfes_token='AAIII',
            status=CompanyEnum.ACTIVE
        )

        company_service = CompanyService(mock_repository)
        company_service.company_repository.get_id = Mock(return_value=True)

        new_company = CompanySchemaIn(
            fantasy_name="Skynet",
            social_name="Skynet SA",
            document="00.000.000/0001-00",
            address="Street X",
            number_address="25",
            complement=None,
            zip_code="99999-99",
            district="Ingleses",
            city="Florianópolis",
            state="SC",
            email="contact@skynet.org",
            phone="55548984863711",
            city_code='0001',
            aliquot=10,
            municipal_registration='000093',
            iss_retained=False,
            licences_n=50,
            api_nfes_token='AAIII',
            status=CompanyEnum.ACTIVE
        )

        created_item = company_service.update(
            id='469264d5-6203-4f2e-aa2e-fdb0d939bc96', company_in=new_company)
        self.assertEqual(created_item.id, uuid.UUID('469264d5-6203-4f2e-aa2e-fdb0d939bc96'))
        self.assertEqual(created_item.fantasy_name, 'Skynet')
        self.assertEqual(created_item.social_name, 'Skynet SA')
        self.assertEqual(created_item.document, '00.000.000/0001-00')
        self.assertEqual(created_item.email, 'contact@skynet.org')
        self.assertEqual(created_item.licences_n, 50)
        self.assertEqual(created_item.status, CompanyEnum.ACTIVE)


    def test_does_not_update_id_not_found(self):
        mock_repository = Mock()
        company_service = CompanyService(mock_repository)
        company_service.company_repository.get_id = Mock(return_value=False)

        new_company = CompanySchemaIn(
            fantasy_name="Skynet",
            social_name="Skynet SA",
            document="00.000.000/0001-00",
            address="Street X",
            number_address="25",
            complement=None,
            zip_code="99999-99",
            district="Ingleses",
            city="Florianópolis",
            state="SC",
            email="contact@skynet.org",
            phone="55548984863711",
            city_code='0001',
            aliquot=10,
            municipal_registration='000093',
            iss_retained=False,
            licences_n=50,
            api_nfes_token='AAIII',
            status=CompanyEnum.ACTIVE
        )

        mock_repository = Mock()
        company_service = CompanyService(mock_repository)
        company_service.company_repository.get_id = Mock(return_value=False)
        with self.assertRaises(ValueError):
            company_service.update(
                id='469264d5-6203-4f2e-aa2e-fdb0d939bc96', company_in=new_company)

    def test_return_get_id_existing(self):
        mock_repository = Mock()
        mock_repository.get_id.return_value = CompanySchemaOut(
            id='469264d5-6203-4f2e-aa2e-fdb0d939bc96',
            fantasy_name="Skynet",
            social_name="Skynet SA",
            document="00.000.000/0001-00",
            address="Street X",
            number_address="25",
            complement=None,
            zip_code="99999-99",
            district="Ingleses",
            city="Florianópolis",
            state="SC",
            email="contact@skynet.org",
            phone="55548984863711",
            city_code='0001',
            aliquot=10,
            municipal_registration='000093',
            iss_retained=False,
            licences_n=50,
            api_nfes_token='AAIII',
            status=CompanyEnum.ACTIVE
        )

        company_service = CompanyService(mock_repository)
        response = company_service.get_id(id='469264d5-6203-4f2e-aa2e-fdb0d939bc96')

        self.assertEqual(response.id, uuid.UUID('469264d5-6203-4f2e-aa2e-fdb0d939bc96'))
        self.assertEqual(response.fantasy_name, 'Skynet')
        self.assertEqual(response.social_name, 'Skynet SA')
        self.assertEqual(response.document, '00.000.000/0001-00')
        self.assertEqual(response.email, 'contact@skynet.org')
        self.assertEqual(response.licences_n, 50)
        self.assertEqual(response.status, CompanyEnum.ACTIVE)


    def test_return_none_get_id_not_existing(self):
        mock_repository = Mock()
        company_service = CompanyService(mock_repository)
        company_service.get_id = Mock(return_value=False)

        response = company_service.get_id(id='469264d5-6203-4f2e-aa2e-fdb0d939bc96')
        self.assertFalse(response)


    def test_return_get_all(self):
        company = CompanySchemaOut(
            id='469264d5-6203-4f2e-aa2e-fdb0d939bc96',
            fantasy_name="Skynet",
            social_name="Skynet SA",
            document="00.000.000/0001-00",
            address="Street X",
            number_address="25",
            complement=None,
            zip_code="99999-99",
            district="Ingleses",
            city="Florianópolis",
            state="SC",
            email="contact@skynet.org",
            phone="55548984863711",
            city_code='0001',
            aliquot=10,
            municipal_registration='000093',
            iss_retained=False,
            licences_n=50,
            api_nfes_token='AAIII',
            status=CompanyEnum.ACTIVE
        )

        mock_repository = Mock()
        mock_repository.get_all.return_value = [company]

        company_service = CompanyService(mock_repository)
        response = company_service.get_all()

        self.assertListEqual(response, [company])
        self.assertIsInstance(response, list)
        self.assertEqual(len(response), 1)

        expected_fields = {
            'id', 'fantasy_name', 'social_name', 'document', 'address',
            'number_address', 'complement', 'zip_code', 'district',
            'city', 'state', 'email', 'phone', 'city_code', 'aliquot',
            'municipal_registration', 'iss_retained', 'licences_n',
            'api_nfes_token', 'status'
        }
        self.assertSetEqual(set(company.dict().keys()), expected_fields)

    def test_return_company_by_user_logged(self):
        mock_repository = Mock()
        mock_repository.company_by_user_logged.return_value = CompanySchemaOut(
            id='469264d5-6203-4f2e-aa2e-fdb0d939bc96',
            fantasy_name="Skynet",
            social_name="Skynet SA",
            document="00.000.000/0001-00",
            address="Street X",
            number_address="25",
            complement=None,
            zip_code="99999-99",
            district="Ingleses",
            city="Florianópolis",
            state="SC",
            email="contact@skynet.org",
            phone="55548984863711",
            city_code='0001',
            aliquot=10,
            municipal_registration='000093',
            iss_retained=False,
            licences_n=50,
            api_nfes_token='AAIII',
            status=CompanyEnum.ACTIVE
        )

        company_service = CompanyService(mock_repository)
        response = company_service.get_company_by_user_logged()

        self.assertEqual(response.id, uuid.UUID('469264d5-6203-4f2e-aa2e-fdb0d939bc96'))
        self.assertEqual(response.fantasy_name, 'Skynet')
        self.assertEqual(response.social_name, 'Skynet SA')
        self.assertEqual(response.document, '00.000.000/0001-00')
        self.assertEqual(response.email, 'contact@skynet.org')
        self.assertEqual(response.licences_n, 50)
        self.assertEqual(response.status, CompanyEnum.ACTIVE)


    def test_return_none_company_by_user_logged_not_existing(self):
        mock_repository = Mock()
        company_service = CompanyService(mock_repository)
        company_service.get_company_by_user_logged = Mock(return_value=False)

        response = company_service.get_company_by_user_logged()
        self.assertFalse(response)