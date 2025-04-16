from datetime import datetime
from uuid import UUID
from pydantic import BaseModel

class TemplateDefinitionDTO(BaseModel):
    uuid: UUID
    name: str
    description: str
    template_body: dict
    version: str
    created_at: datetime