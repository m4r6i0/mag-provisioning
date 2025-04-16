import unittest
from unittest.mock import MagicMock
from sqlalchemy.orm import Session

from src.services.audit_log_service import AuditLogService
from src.entities.audit_log import AuditLog
from src.repositories.audit_log_repository import AuditLogRepository


class TestAuditLogService(unittest.TestCase):
    def setUp(self):
        self.mock_session = MagicMock(spec=Session)
        self.mock_audit_log_repository = MagicMock(spec=AuditLogRepository)
        self.audit_log_service = AuditLogService(self.mock_audit_log_repository, self.mock_session)

    def test_create(self):
        # Arrange
        audit_log = AuditLog(uuid="id")
        self.mock_audit_log_repository.create.return_value = audit_log
        # Act
        result = self.audit_log_service.create(audit_log)
        # Assert
        self.mock_audit_log_repository.create.assert_called_once_with(audit_log)
        self.assertEqual(result, audit_log)