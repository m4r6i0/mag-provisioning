from uuid import UUID
from datetime import datetime
from pydantic import BaseModel

class AuditLogDTO(BaseModel):
    uuid: UUID
    user_id: UUID
    action: str
    entity_type: str
    entity_id: UUID
    description: str
    timestamp: datetime