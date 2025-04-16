import unittest
from unittest.mock import MagicMock
from sqlalchemy.orm import Session

from src.services.resource_dependency_service import ResourceDependencyService
from src.entities.resource_dependency import ResourceDependency
from src.repositories.resource_dependency_repository import ResourceDependencyRepository

class TestResourceDependencyService(unittest.TestCase):
    def setUp(self):
        self.mock_session = MagicMock(spec=Session)
        self.mock_session.add = MagicMock()
        self.mock_resource_dependency_repository = MagicMock(
            spec=ResourceDependencyRepository
        )
        self.resource_dependency_service = ResourceDependencyService(
            self.mock_session, self.mock_resource_dependency_repository
        )
    def test_create(self):
        # Arrange
        resource_dependency = ResourceDependency(resource_id="id1")
        self.mock_resource_dependency_repository.create.return_value = resource_dependency
        # Act
        result = self.resource_dependency_service.create(resource_dependency)
        # Assert
        self.mock_resource_dependency_repository.create.assert_called_once_with(resource_dependency)
        self.assertEqual(result, resource_dependency)
