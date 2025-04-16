from sqlalchemy.orm import Session
from src.entities.execution_log import ExecutionLog
from uuid import UUID

class ExecutionLogRepository:
    def __init__(self, session: Session):
        self.session = session

    def find_by_id(self, id: UUID) -> ExecutionLog:
        return self.session.query(ExecutionLog).filter(ExecutionLog.uuid == id).first()

    def find_all(self) -> list[ExecutionLog]:
        return self.session.query(ExecutionLog).all()

    def create(self, execution_log: ExecutionLog) -> ExecutionLog:
        self.session.add(execution_log)
        self.session.commit()
        self.session.refresh(execution_log)
        return execution_log

    def update(self, execution_log: ExecutionLog) -> ExecutionLog:
        self.session.merge(execution_log)
        self.session.commit()
        self.session.refresh(execution_log)
        return execution_log

    def delete(self, id: UUID) -> None:
        execution_log = self.find_by_id(id)
        if execution_log:
            self.session.delete(execution_log)
            self.session.commit()