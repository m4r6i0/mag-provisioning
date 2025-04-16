from typing import List
from fastapi import APIRouter, Depends, HTTPException
from src.services.audit_log_service import AuditLogService
from src.dtos.audit_log_dto import AuditLogDTO
from uuid import UUID
from sqlalchemy.orm import Session
from src.infrastructure.database import get_db

router = APIRouter()

class AuditLogController:
    def __init__(self, audit_log_service: AuditLogService = Depends()):
        self.audit_log_service = audit_log_service

    @router.get("/v1/audit-logs", response_model=List[AuditLogDTO])
    def get_all_audit_logs(self, db: Session = Depends(get_db)):
        try:
            audit_logs = self.audit_log_service.find_all(db)
            return [AuditLogDTO.model_validate(log) for log in audit_logs]
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @router.get("/v1/audit-logs/{uuid}", response_model=AuditLogDTO)
    def get_audit_log_by_id(self, uuid: UUID, db: Session = Depends(get_db)):
        try:
            audit_log = self.audit_log_service.find_by_id(uuid, db)
            if not audit_log:
                raise HTTPException(status_code=404, detail="Audit log not found")
            return AuditLogDTO.model_validate(audit_log)
        except HTTPException as http_ex:
            raise http_ex
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))