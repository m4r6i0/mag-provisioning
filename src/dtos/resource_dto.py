from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class ResourceDTO(BaseModel):
    uuid: UUID
    request_id: UUID
    resource_type: str
    resource_name: str
    cloud_provider: str
    status: str
    created_at: datetime
    updated_at: datetime