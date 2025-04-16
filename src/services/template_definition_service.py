from sqlalchemy.orm import Session
from src.entities.template_definition import TemplateDefinition
from src.repositories.template_definition_repository import TemplateDefinitionRepository
from typing import List
from uuid import UUID


class TemplateDefinitionService:
    def __init__(self, session: Session):
        self.template_definition_repository: TemplateDefinitionRepository = TemplateDefinitionRepository(session)

    def find_all(self) -> List[TemplateDefinition]:
        return self.template_definition_repository.find_all()

    def find_by_id(self, uuid: UUID) -> TemplateDefinition:
        return self.template_definition_repository.find_by_id(uuid)
    
    def create(self, template_definition: TemplateDefinition):
        return self.template_definition_repository.create(template_definition)