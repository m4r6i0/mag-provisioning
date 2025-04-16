import unittest
from unittest.mock import MagicMock
from sqlalchemy.orm import Session

from src.services.execution_log_service import ExecutionLogService
from src.entities.execution_log import ExecutionLog
from src.repositories.execution_log_repository import ExecutionLogRepository

class TestExecutionLogService(unittest.TestCase):
    def setUp(self):
        self.mock_session = MagicMock(spec=Session)
        self.mock_session.add = MagicMock()
        self.mock_execution_log_repository = ExecutionLogRepository(self.mock_session)
        self.execution_log_service = ExecutionLogService(self.mock_session)


    def test_create(self):
        # Arrange
        execution_log = ExecutionLog(uuid="id",  message="log")
        self.mock_session.add.return_value = execution_log
        # Act
        result = self.execution_log_service.create(execution_log)
        # Assert
        self.mock_session.add.assert_called_once_with(execution_log)
        self.mock_session.commit.assert_called_once()
        self.assertEqual(result, execution_log)
