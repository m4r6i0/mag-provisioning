from datetime import datetime
from uuid import UUID
from pydantic import BaseModel

class ProvisionRequestDTO(BaseModel):
    uuid: UUID
    user_id: UUID
    request_time: datetime
    status: str
    priority: int
    resource_type: str
    parameters: dict
    worker_id: UUID
    last_update: datetime