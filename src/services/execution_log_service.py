from sqlalchemy.orm import Session
from src.entities.execution_log import ExecutionLog
from src.repositories.execution_log_repository import ExecutionLogRepository

class ExecutionLogService:
    def __init__(self, session: Session):
        self.repository = ExecutionLogRepository(session)

    def find_all(self) -> list[ExecutionLog]:
        return self.repository.find_all()

    def find_by_id(self, uuid: str) -> ExecutionLog:
        return self.repository.find_by_id(uuid)