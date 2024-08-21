import unittest
from unittest.mock import Mock
from app.services.address_instructor_service import AddressInstructorService
from db.models import AddressInstructor


class TestAddressInstructorService(unittest.TestCase):
    def test_create(self):
        mock_repository = Mock()
        mock_repository.create.return_value = AddressInstructor(
            id='f26c6ce1-a335-4896-97d0-d2d483379fdf',
            instructor_id='29241ac0-6a39-42d0-887b-6d5a3ec31df4',
            address='STREET X',
            number='12',
            complement=None,
            zip_code=None,
            district=None,
            city=None,
            state=None,
        )

        address_instructor_service = AddressInstructorService(
            address_instructor_repository=mock_repository
        )

        new_address = AddressInstructor(
            address='STREET X',
            number='12',
            complement=None,
            zip_code=None,
            district=None,
            city=None,
            state=None,
        )

        created_item = address_instructor_service.create(
            address_in=new_address,
            instructor_id='29241ac0-6a39-42d0-887b-6d5a3ec31df4')
        self.assertEqual(
            created_item.id, 'f26c6ce1-a335-4896-97d0-d2d483379fdf')

    def test_update(self):
        mock_repository = Mock()
        mock_repository.update.return_value = AddressInstructor(
            id='f26c6ce1-a335-4896-97d0-d2d483379fdf',
            instructor_id='29241ac0-6a39-42d0-887b-6d5a3ec31df4',
            address='STREET X',
            number='12',
            complement=None,
            zip_code=None,
            district=None,
            city=None,
            state=None,
        )

        address_instructor_service = AddressInstructorService(
            address_instructor_repository=mock_repository
        )

        mock_exists_function = Mock(return_value=True)
        address_instructor_service.address_instructor_repository.get_id = mock_exists_function

        new_address = AddressInstructor(
            address='STREET X',
            number='12',
            complement=None,
            zip_code=None,
            district=None,
            city=None,
            state=None,
        )

        created_item = address_instructor_service.update(
            id='f26c6ce1-a335-4896-97d0-d2d483379fdf', address_in=new_address)
        self.assertEqual(
            created_item.id, 'f26c6ce1-a335-4896-97d0-d2d483379fdf')

        mock_exists_function.return_value = False
        with self.assertRaises(ValueError):
            address_instructor_service.update(
                id='f26c6ce1-a335-4896-97d0-d2d483379fdf', address_in=new_address)
