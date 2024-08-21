import unittest
from unittest.mock import Mock
from app.constants.enums.permission_enum import PermissionEnum
from app.constants.enums.status_enum import StatusEnum
from db.models import User
from app.services.user_service import UserService


class TestUserService(unittest.TestCase):
    def test_create(self):
        mock_repository = Mock()
        mock_email = Mock()
        mock_exists_function = Mock(return_value=False)

        mock_repository.create.return_value = User(
            id='18b941d7-6d85-4f84-a8fa-13b9f71d6806',
            company_id='469264d5-6203-4f2e-aa2e-fdb0d939bc96',
            fullname="John Connor",
            document="000.000.000-10",
            email="john.connor@skynet.com",
            permission=PermissionEnum.ADMIN,
            image_path=None,
            position="LEAD",
            status=StatusEnum.ACTIVE)

        user_service = UserService(
            user_repository=mock_repository, mailer=mock_email)
        user_service.user_repository.get_document = mock_exists_function
        user_service.user_repository.get_email = mock_exists_function
        user_service.mailer.sender = mock_exists_function

        new_user = User(
            company_id='469264d5-6203-4f2e-aa2e-fdb0d939bc96',
            fullname="John Connor",
            document="000.000.000-10",
            email="john.connor@skynet.com",
            permission="ADMIN",
            image_path=None,
            position="LEAD",
        )
        created_item = user_service.create(new_user)
        self.assertEqual(
            created_item.id, '18b941d7-6d85-4f84-a8fa-13b9f71d6806')
        self.assertEqual(created_item.fullname, 'John Connor')
        mock_exists_function.return_value = True
        with self.assertRaises(ValueError):
            user_service.create(new_user)

    def test_update(self):
        mock_repository = Mock()
        mock_email = Mock()
        mock_exists_function = Mock(return_value=True)

        mock_repository.update.return_value = User(
            id='18b941d7-6d85-4f84-a8fa-13b9f71d6806',
            company_id='469264d5-6203-4f2e-aa2e-fdb0d939bc96',
            fullname="John Connor",
            document="000.000.000-10",
            email="john.connor@skynet.com",
            permission=PermissionEnum.ADMIN,
            image_path=None,
            position="LEADER",
            status=StatusEnum.ACTIVE)

        user_service = UserService(
            user_repository=mock_repository, mailer=mock_email)
        user_service.user_repository.get_id = mock_exists_function

        new_user = User(
            company_id='469264d5-6203-4f2e-aa2e-fdb0d939bc96',
            fullname="John Connor",
            document="000.000.000-10",
            email="john.connor@skynet.com",
            permission="ADMIN",
            image_path=None,
            position="LEADER",
            status=StatusEnum.ACTIVE
        )
        created_item = user_service.update(
            id='18b941d7-6d85-4f84-a8fa-13b9f71d6806', user_in=new_user)
        self.assertEqual(
            created_item.id, '18b941d7-6d85-4f84-a8fa-13b9f71d6806')

        mock_exists_function.return_value = False
        with self.assertRaises(ValueError):
            user_service.update(
                id='18b941d7-6d85-4f84-a8fa-13b9f71d6806', user_in=new_user)
