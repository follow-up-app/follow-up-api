import unittest
from unittest.mock import Mock
from app.constants.enums.partenal_enum import PartenalEnum
from app.services.responsible_contract_service import ResponsibleContractService
from db.models import ResponsibleContract


class TestResponsibleContractService(unittest.TestCase):
    def test_create(self):
        mock_repository = Mock()
        mock_repository.create.return_value = ResponsibleContract(
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

        responsible_contract_service = ResponsibleContractService(
            responsible_contract_repository=mock_repository
        )

        new_responsible = ResponsibleContract(
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
        created_item = responsible_contract_service.create(
            'ef83d3dd-d7fc-41dd-8cc2-4e69ef67b594', new_responsible)

        self.assertEqual(
            created_item.id, 'c54112e3-abf7-42e7-9b40-9fa3338c4adc')
        self.assertEqual(created_item.fullname, 'Mother Anakin')

    def test_update(self):
        mock_repository = Mock()
        mock_repository.update.return_value = ResponsibleContract(
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

        responsible_contract_service = ResponsibleContractService(
            responsible_contract_repository=mock_repository
        )
        mock_exists_function = Mock(return_value=True)
        responsible_contract_service.responsible_contract_repository.get_id = mock_exists_function

        new_responsible = ResponsibleContract(
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
        created_item = responsible_contract_service.update(
            id='c54112e3-abf7-42e7-9b40-9fa3338c4adc', responsible_contract_in=new_responsible)
        self.assertEqual(
            created_item.id, 'c54112e3-abf7-42e7-9b40-9fa3338c4adc')

        mock_exists_function.return_value = False
        with self.assertRaises(ValueError):
            responsible_contract_service.update(
                id='c54112e3-abf7-42e7-9b40-9fa3338c4adc', responsible_contract_in=new_responsible)
