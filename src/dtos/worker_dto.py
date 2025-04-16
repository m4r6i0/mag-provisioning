from datetime import datetime
from uuid import UUID
from pydantic import BaseModel

class WorkerDTO(BaseModel):
    uuid: UUID
    ip_address: str
    status: str
    last_seen: datetime