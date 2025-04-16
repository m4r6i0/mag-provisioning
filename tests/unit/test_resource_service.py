import unittest
from unittest.mock import MagicMock
from sqlalchemy.orm import Session
from src.services.resource_service import ResourceService
from src.entities.resource import Resource
from src.repositories.resource_repository import ResourceRepository

class TestResourceService(unittest.TestCase):
    def setUp(self):
        self.mock_session = MagicMock(spec=Session)
        self.mock_session.add = MagicMock()
        self.mock_resource_repository = MagicMock(spec=ResourceRepository)
        self.resource_repository = ResourceRepository(self.mock_session)
        self.resource_service = ResourceService(self.mock_session)

    def test_create(self):
        # Arrange
        resource = Resource(uuid="resource-id", resource_type="vm", resource_name="vm-dev-01", cloud_provider="AZURE", status="pending")
        self.mock_session.add.return_value = resource
        # Act
        result = self.resource_service.create(resource)        
        # Assert
        self.mock_session.commit.assert_called_once()
        self.mock_session.add.assert_called_once_with(resource)
        self.assertEqual(result, resource)
