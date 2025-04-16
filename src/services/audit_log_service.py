from sqlalchemy.orm import Session
from src.entities.audit_log import AuditLog
from src.repositories.audit_log_repository import AuditLogRepository
from uuid import UUID

class AuditLogService:
    def __init__(self, audit_log_repository: AuditLogRepository, session: Session):
        self.audit_log_repository = audit_log_repository
        self.session = session

    def find_all(self):
        return self.audit_log_repository.find_all()

    def find_by_id(self, audit_log_id: UUID):
        return self.audit_log_repository.find_by_id(audit_log_id)