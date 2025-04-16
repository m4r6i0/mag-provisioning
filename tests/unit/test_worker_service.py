import unittest
from unittest.mock import MagicMock
from src.services.worker_service import WorkerService
from src.entities.worker import Worker
from src.repositories.worker_repository import WorkerRepository
 

class TestWorkerService(unittest.TestCase):
    def setUp(self):
        self.mock_worker_repository = MagicMock(spec=WorkerRepository)
        self.worker_service = WorkerService(self.mock_worker_repository)
    def test_create(self):

        # Arrange
        worker = Worker(uuid="worker-az01", ip_address="10.10.1.42")
        self.mock_worker_repository.create.return_value = worker
        # Act
        result = self.worker_service.create(worker)
        # Assert
        self.mock_worker_repository.create.assert_called_once_with(worker)
        self.assertEqual(result, worker)