import unittest
from unittest.mock import Mock
from app.services.address_contract_service import AddressContractService
from db.models import AddressContract


class TestAddressContractService(unittest.TestCase):
    def test_create(self):
        mock_repository = Mock()
        mock_repository.create.return_value = AddressContract(
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

        address_contract_service = AddressContractService(
            address_contract_repository=mock_repository
        )

        new_address = AddressContract(
            responsible_contract_id='c54112e3-abf7-42e7-9b40-9fa3338c4adc',
            address='STREET X',
            number='12',
            complement=None,
            zip_code=None,
            district=None,
            city=None,
            state=None,
        )
        created_item = address_contract_service.create(
            address_in=new_address,
            contractor_id='ef83d3dd-d7fc-41dd-8cc2-4e69ef67b594')
        self.assertEqual(
            created_item.id, 'f26c6ce1-a335-4896-97d0-d2d483379fdf')

    def test_update(self):
        mock_repository = Mock()
        mock_repository.update.return_value = AddressContract(
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

        address_contract_service = AddressContractService(
            address_contract_repository=mock_repository
        )

        mock_exists_function = Mock(return_value=True)
        address_contract_service.address_contract_repository.get_id = mock_exists_function

        new_address = AddressContract(
            responsible_contract_id='c54112e3-abf7-42e7-9b40-9fa3338c4adc',
            address='STREET X',
            number='12',
            complement=None,
            zip_code=None,
            district=None,
            city=None,
            state=None,
        )

        created_item = address_contract_service.update(
            id='f26c6ce1-a335-4896-97d0-d2d483379fdf', address_in=new_address)
        self.assertEqual(
            created_item.id, 'f26c6ce1-a335-4896-97d0-d2d483379fdf')

        mock_exists_function.return_value = False
        with self.assertRaises(ValueError):
            address_contract_service.update(
                id='f26c6ce1-a335-4896-97d0-d2d483379fdf', address_in=new_address)
