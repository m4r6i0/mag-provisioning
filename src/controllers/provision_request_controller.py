from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.services.provision_request_service import ProvisionRequestService
from src.dtos.provision_request_dto import ProvisionRequestDTO
from src.infrastructure.database import get_db
from uuid import UUID

router = APIRouter()

class ProvisionRequestController:
    def __init__(self, service: ProvisionRequestService = Depends()):
        self.service = service

    @router.get("/v1/provision-requests", response_model=List[ProvisionRequestDTO])
    def get_all_provision_requests(self, db: Session = Depends(get_db)):
        try:
            provision_requests = self.service.find_all(db)
            return provision_requests
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @router.get("/v1/provision-requests/{uuid}", response_model=ProvisionRequestDTO)
    def get_provision_request_by_id(self, uuid: UUID, db: Session = Depends(get_db)):
        try:
            provision_request = self.service.find_by_id(db, uuid)
            if provision_request is None:
                raise HTTPException(status_code=404, detail="Provision request not found")
            return provision_request
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))