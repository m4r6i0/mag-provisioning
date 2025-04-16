from sqlalchemy.orm import Session
from src.entities.template_definition import TemplateDefinition
from src.repositories.template_definition_repository import TemplateDefinitionRepository
from typing import List
from uuid import UUID


class TemplateDefinitionService:
    def __init__(self, session: Session):
        self.repository: TemplateDefinitionRepository = TemplateDefinitionRepository(session)

    def find_all(self) -> List[TemplateDefinition]:
        return self.repository.find_all()

    def find_by_id(self, uuid: UUID) -> TemplateDefinition:
        return self.repository.find_by_id(uuid)