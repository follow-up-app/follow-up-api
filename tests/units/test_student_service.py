import unittest
from unittest.mock import Mock
from app.constants.enums.genere_enum import GenereEnum
from app.constants.enums.partenal_enum import PartenalEnum
from app.constants.enums.status_enum import StatusEnum
from app.services.address_contract_service import AddressContractService
from app.services.contractor_service import ContractorService
from app.services.responsible_contract_service import ResponsibleContractService
from app.services.student_service import StudentService
from db.models import AddressContract, Contractor, ResponsibleContract, Student


class TestStudentService(unittest.TestCase):
    def test_create(self):
        mock_repository = Mock()
        mock_repository.create.return_value = Student(
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
        mock_contractor_repository.create.return_value = Contractor(
            id='ef83d3dd-d7fc-41dd-8cc2-4e69ef67b594',
            company_id='469264d5-6203-4f2e-aa2e-fdb0d939bc96'
        )

        mock_reponsible_repository = Mock()
        mock_reponsible_repository.create.return_value = ResponsibleContract(
            id='c54112e3-abf7-42e7-9b40-9fa3338c4adc',
            contractor_id='ef83d3dd-d7fc-41dd-8cc2-4e69ef67b594',
            fullname='Mother Anakin',
            birthday=None,
            document='101.202.301-10',
            indentity_number='0001',
            org_exp=None,
            uf_exp=None,
            nationality=None,
            email=None,
            phone=None,
            bond=PartenalEnum.MOTHER,
            main_contract=True,
        )

        mock_address_repository = Mock()
        mock_address_repository.create.return_value = AddressContract(
            id='f26c6ce1-a335-4896-97d0-d2d483379fdf',
            contractor_id='ef83d3dd-d7fc-41dd-8cc2-4e69ef67b594',
            responsible_contract_id='c54112e3-abf7-42e7-9b40-9fa3338c4adc',
            address='STREET X',
            number='12',
            complement=None,
            zip_code=None,
            district=None,
            city=None,
            state=None,
        )

        contractor_service = ContractorService(
            contractor_repository=mock_contractor_repository)

        responsible_contract_service = ResponsibleContractService(
            responsible_contract_repository=mock_reponsible_repository
        )

        address_contract_service = AddressContractService(
            address_contract_repository=mock_address_repository
        )

        student_service = StudentService(
            student_repository=mock_repository,
            contractor_service=contractor_service,
            responsible_contract_service=responsible_contract_service,
            address_contract_service=address_contract_service
        )

        mock_exists_function = Mock(return_value=False)
        student_service.student_repository.get_document = mock_exists_function

        new_student = Student(
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
        )
        created_item = student_service.create(new_student)
        self.assertEqual(
            created_item.id, '18b941d7-6d85-4f84-a8fa-13b9f71d6806')
        self.assertEqual(created_item.fullname, 'Anakin Skywalker')

        mock_exists_function.return_value = True
        with self.assertRaises(ValueError):
            student_service.create(new_student)

    def test_update(self):
        mock_repository = Mock()
        mock_repository.update.return_value = Student(
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
        mock_contractor_repository.create.return_value = Contractor(
            id='ef83d3dd-d7fc-41dd-8cc2-4e69ef67b594',
            company_id='469264d5-6203-4f2e-aa2e-fdb0d939bc96'
        )

        mock_reponsible_repository = Mock()
        mock_reponsible_repository.create.return_value = ResponsibleContract(
            id='c54112e3-abf7-42e7-9b40-9fa3338c4adc',
            contractor_id='ef83d3dd-d7fc-41dd-8cc2-4e69ef67b594',
            fullname='Mother Anakin',
            birthday=None,
            document='101.202.301-10',
            indentity_number='0001',
            org_exp=None,
            uf_exp=None,
            nationality=None,
            email=None,
            phone=None,
            bond=PartenalEnum.MOTHER,
            main_contract=True,
        )

        mock_address_repository = Mock()
        mock_address_repository.create.return_value = AddressContract(
            id='f26c6ce1-a335-4896-97d0-d2d483379fdf',
            contractor_id='ef83d3dd-d7fc-41dd-8cc2-4e69ef67b594',
            responsible_contract_id='c54112e3-abf7-42e7-9b40-9fa3338c4adc',
            address='STREET X',
            number='12',
            complement=None,
            zip_code=None,
            district=None,
            city=None,
            state=None,
        )

        contractor_service = ContractorService(
            contractor_repository=mock_contractor_repository)

        responsible_contract_service = ResponsibleContractService(
            responsible_contract_repository=mock_reponsible_repository
        )

        address_contract_service = AddressContractService(
            address_contract_repository=mock_address_repository
        )

        student_service = StudentService(
            student_repository=mock_repository,
            contractor_service=contractor_service,
            responsible_contract_service=responsible_contract_service,
            address_contract_service=address_contract_service
        )
        mock_exists_function = Mock(return_value=True)
        student_service.student_repository.get_id = mock_exists_function

        new_student = Student(
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
        )

        created_item = student_service.update(
            id='18b941d7-6d85-4f84-a8fa-13b9f71d6806', student_in=new_student)
        self.assertEqual(
            created_item.id, '18b941d7-6d85-4f84-a8fa-13b9f71d6806')

        mock_exists_function.return_value = False
        with self.assertRaises(ValueError):
            student_service.update(
                id='18b941d7-6d85-4f84-a8fa-13b9f71d6806', student_in=new_student)
