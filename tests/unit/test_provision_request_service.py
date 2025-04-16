import unittest
from unittest.mock import MagicMock
from sqlalchemy.orm import Session
from uuid import uuid4

from src.services.provision_request_service import ProvisionRequestService
from src.entities.provision_request import ProvisionRequest
from src.repositories.provision_request_repository import ProvisionRequestRepository

class TestProvisionRequestService(unittest.TestCase):
    def setUp(self):
        self.mock_provision_request_repository = MagicMock(spec=ProvisionRequestRepository)
        self.mock_session = MagicMock(spec=Session)
        self.service = ProvisionRequestService(self.mock_session, self.mock_provision_request_repository)

    def test_find_all(self):
        # Arrange
        expected_requests = [
            ProvisionRequest(uuid=str(uuid4()), request_time="2025-04-09T13:00:00Z", status="pending", priority=1, resource_type="vm-ubuntu-lts", parameters={})
        ]
        self.mock_provision_request_repository.find_all.return_value = expected_requests        

        # Act
        result = self.service.find_all()

        # Assert
        self.mock_provision_request_repository.find_all.assert_called_once()
        self.assertEqual(result, expected_requests)

    def test_find_by_id(self):
        # Arrange
        request_id = str(uuid4())
        expected_request = ProvisionRequest(uuid=request_id, request_time="2025-04-09T13:00:00Z", status="pending", priority=1, resource_type="vm-ubuntu-lts", parameters={})
        self.mock_provision_request_repository.find_by_id.return_value = expected_request

        # Act
        result = self.service.find_by_id(request_id)

        # Assert
        self.mock_provision_request_repository.find_by_id.assert_called_once_with(request_id)
        self.assertEqual(result, expected_request)