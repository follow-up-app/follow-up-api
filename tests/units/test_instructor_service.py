import unittest
from unittest.mock import Mock
from app.constants.enums.permission_enum import PermissionEnum
from app.constants.enums.status_enum import StatusEnum
from app.services.address_instructor_service import AddressInstructorService
from app.services.instructor_service import InstructorService
from app.services.user_service import UserService
from db.models import AddressInstructor, Instructor, User


class TestInstructorService(unittest.TestCase):
    def test_create(self):
        mock_repository = Mock()
        mock_repository.create.return_value = Instructor(
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
        mock_user_repository.create.return_value = User(
            id='18b941d7-6d85-4f84-a8fa-13b9f71d6806',
            company_id='469264d5-6203-4f2e-aa2e-fdb0d939bc96',
            fullname="Obi Wan knobe",
            document="101.202.301-10",
            email="obi.wan@jedi.com",
            permission=PermissionEnum.INSTRUCTOR,
            image_path=None,
            position="PROFISSIONAL",
            status=StatusEnum.ACTIVE
        )
        mock_email = Mock()

        mock_address_repository = Mock()
        mock_address_repository.create.return_value = AddressInstructor(
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

        user_service = UserService(
            user_repository=mock_user_repository, mailer=mock_email)

        instructor_payment_repository = Mock()

        instructor_service = InstructorService(
            instructor_repository=mock_repository,
            user_service=user_service,
            address_instructor_repository=mock_address_repository,
            instructor_payment_repository=instructor_payment_repository
        )

        instructor_service.user_service.create = mock_user_repository

        new_instructor = Instructor(
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
        )
        created_item = instructor_service.create(new_instructor)
        self.assertEqual(
            created_item.id, '29241ac0-6a39-42d0-887b-6d5a3ec31df4')
        self.assertEqual(created_item.fullname, 'Obi Wan knobe')

        with self.assertRaises(ValueError):
            instructor_service.user_service.create = Mock(return_value=False)
            instructor_service.create(new_instructor)

    def test_update(self):
        mock_repository = Mock()
        mock_repository.update.return_value = Instructor(
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
        mock_user_repository.create.return_value = User(
            id='18b941d7-6d85-4f84-a8fa-13b9f71d6806',
            company_id='469264d5-6203-4f2e-aa2e-fdb0d939bc96',
            fullname="Obi Wan knobe",
            document="101.202.301-10",
            email="obi.wan@jedi.com",
            permission=PermissionEnum.INSTRUCTOR,
            image_path=None,
            position="PROFISSIONAL",
            status=StatusEnum.ACTIVE
        )
        mock_email = Mock()

        mock_address_repository = Mock()
        mock_address_repository.create.return_value = AddressInstructor(
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

        user_service = UserService(
            user_repository=mock_user_repository, mailer=mock_email)
        address_instructor_service = AddressInstructorService(
            address_instructor_repository=mock_address_repository)

        instructor_payment_repository = Mock()
        instructor_service = InstructorService(
            instructor_repository=mock_repository,
            user_service=user_service,
            address_instructor_repository=mock_address_repository,
            instructor_payment_repository=instructor_payment_repository
        )

        mock_exists_function = Mock(return_value=True)
        instructor_service.instructor_repository.get_id = mock_exists_function

        new_instructor = Instructor(
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
        )

        created_item = instructor_service.update(
            id='29241ac0-6a39-42d0-887b-6d5a3ec31df4', instructor_in=new_instructor)
        self.assertEqual(
            created_item.id, '29241ac0-6a39-42d0-887b-6d5a3ec31df4')

        mock_exists_function.return_value = False
        with self.assertRaises(ValueError):
            instructor_service.update(
                id='29241ac0-6a39-42d0-887b-6d5a3ec31df4', instructor_in=new_instructor)
