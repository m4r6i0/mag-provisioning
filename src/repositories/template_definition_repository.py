from sqlalchemy.orm import Session
from src.entities.template_definition import TemplateDefinition
from uuid import UUID, uuid4


class TemplateDefinitionRepository:
    def __init__(self, session: Session):
        self.session = session

    def find_by_id(self, uuid: str) -> TemplateDefinition | None:
        return self.session.query(TemplateDefinition).filter(TemplateDefinition.uuid == uuid).first()

    def find_all(self) -> list[TemplateDefinition]:
        return self.session.query(TemplateDefinition).all()

    def create(self, template_definition: TemplateDefinition) -> TemplateDefinition:
        self.session.add(template_definition)
        self.session.commit()
        self.session.refresh(template_definition)
        return template_definition

    def update(self, template_definition: TemplateDefinition) -> TemplateDefinition:
        self.session.commit()
        self.session.refresh(template_definition)
        return template_definition

    def delete(self, template_definition: TemplateDefinition):
        self.session.delete(template_definition)
        self.session.commit()