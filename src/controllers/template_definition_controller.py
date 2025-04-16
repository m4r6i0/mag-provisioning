from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from src.services.template_definition_service import TemplateDefinitionService
from src.dtos.template_definition_dto import TemplateDefinitionDTO
from uuid import UUID
from sqlalchemy.orm import Session
from src.infrastructure.database import get_db

router = APIRouter(prefix="/v1/template-definitions", tags=["Template Definitions"])


class TemplateDefinitionController:
    def __init__(self, service: TemplateDefinitionService):
        self.service = service

    @router.get("/", response_model=List[TemplateDefinitionDTO])
    def find_all(
        self, db: Session = Depends(get_db)
    ) -> List[TemplateDefinitionDTO]:
        try:
            self.service.db = db
            return self.service.find_all()
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
            )

    @router.get("/{uuid}", response_model=TemplateDefinitionDTO)
    def find_by_id(
        self, uuid: UUID, db: Session = Depends(get_db)
    ) -> TemplateDefinitionDTO:
        try:
            self.service.db = db
            result = self.service.find_by_id(uuid)
            if result is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Template Definition not found",
                )
            return result
        except HTTPException as http_exception:
            raise http_exception
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
            )


def get_template_definition_controller(
    db: Session = Depends(get_db),
):
    template_definition_service = TemplateDefinitionService(db)
    return TemplateDefinitionController(template_definition_service)