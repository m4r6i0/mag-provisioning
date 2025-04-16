import unittest
from unittest.mock import MagicMock
from src.repositories.user_repository import UserRepository
from src.entities.user import User
from sqlalchemy.orm import Session
from uuid import uuid4

class TestUserRepository(unittest.TestCase):
    def setUp(self):
        self.mock_session = MagicMock(spec=Session)
        self.repository = UserRepository(self.mock_session)

    def test_find_by_name(self):
        # Arrange
        user_name = "automacao-provedor-x"
        expected_user = User(uuid=str(uuid4()), name=user_name)
        self.mock_session.query.return_value.filter.return_value.first.return_value = expected_user

        # Act
        result = self.repository.find_by_name(user_name)

        # Assert
        self.mock_session.query.assert_called_once()
        self.assertEqual(result, expected_user)

    def test_find_by_id(self):
        # Arrange
        user_id = str(uuid4())
        expected_user = User(uuid=user_id, name="automacao-provedor-x")
        self.mock_session.query.return_value.filter.return_value.first.return_value = expected_user

        # Act
        result = self.repository.find_by_id(user_id)

        # Assert
        self.mock_session.query.assert_called_once()
        self.assertEqual(result, expected_user)