from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class ResourceDependencyDTO(BaseModel):
    uuid: UUID
    resource_id: UUID
    depends_on_id: UUID