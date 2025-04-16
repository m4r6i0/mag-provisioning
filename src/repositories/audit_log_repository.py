from sqlalchemy.orm import Session
from src.entities.audit_log import AuditLog
from uuid import UUID

class AuditLogRepository:
    def __init__(self, session: Session):
        self.session = session

    def find_by_id(self, id: UUID) -> AuditLog:
        return self.session.query(AuditLog).filter(AuditLog.uuid == id).first()

    def find_all(self) -> list[AuditLog]:
        return self.session.query(AuditLog).all()

    def create(self, audit_log: AuditLog) -> AuditLog:
        self.session.add(audit_log)
        self.session.commit()
        self.session.refresh(audit_log)
        return audit_log

    def update(self, audit_log: AuditLog) -> AuditLog:
        self.session.merge(audit_log)
        self.session.commit()
        self.session.refresh(audit_log)
        return audit_log

    def delete(self, id: UUID) -> None:
        audit_log = self.find_by_id(id)
        if audit_log:
            self.session.delete(audit_log)
            self.session.commit()