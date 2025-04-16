from typing import List
from fastapi import APIRouter, Depends, HTTPException
from src.services.resource_service import ResourceService
from src.dtos.resource_dto import ResourceDTO
from uuid import UUID
from sqlalchemy.orm import Session
from src.infrastructure.database import get_db

router = APIRouter()

class ResourceController:
    def __init__(self, resource_service: ResourceService = Depends()):
        self.resource_service = resource_service

    @router.get("/v1/resources", response_model=List[ResourceDTO])
    def find_all(self, db: Session = Depends(get_db)):
        try:
            return self.resource_service.find_all(db)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @router.get("/v1/resources/{uuid}", response_model=ResourceDTO)
    def find_by_id(self, uuid: UUID, db: Session = Depends(get_db)):
        try:
            resource = self.resource_service.find_by_id(db, uuid)
            if resource is None:
                raise HTTPException(status_code=404, detail="Resource not found")
            return resource
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

resource_controller = ResourceController()