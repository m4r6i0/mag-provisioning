from uuid import UUID
from pydantic import BaseModel

class ResourceTagDTO(BaseModel):
    uuid: UUID
    resource_id: UUID
    tag_key: str
    tag_value: str