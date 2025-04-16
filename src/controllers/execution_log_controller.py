from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from src.services.execution_log_service import ExecutionLogService
from src.dtos.execution_log_dto import ExecutionLogDTO
from uuid import UUID
from sqlalchemy.orm import Session
from src.infrastructure.database import get_db

router = APIRouter(prefix="/v1/execution-logs", tags=["Execution Logs"])


class ExecutionLogController:
    def __init__(self, execution_log_service: ExecutionLogService = Depends()):
        self.execution_log_service = execution_log_service

    @router.get("/", response_model=List[ExecutionLogDTO])
    def get_all_execution_logs(self, db: Session = Depends(get_db)):
        try:
            execution_logs = self.execution_log_service.find_all(db)
            return [ExecutionLogDTO.model_validate(execution_log) for execution_log in execution_logs]
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    @router.get("/{uuid}", response_model=ExecutionLogDTO)
    def get_execution_log_by_id(self, uuid: UUID, db: Session = Depends(get_db)):
        try:
            execution_log = self.execution_log_service.find_by_id(db, uuid)
            if execution_log is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Execution Log not found")
            return ExecutionLogDTO.model_validate(execution_log)
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))