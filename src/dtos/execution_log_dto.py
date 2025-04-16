from uuid import UUID
from datetime import datetime
from pydantic import BaseModel

class ExecutionLogDTO(BaseModel):
    uuid: UUID
    request_id: UUID
    worker_id: UUID
    log_message: str
    log_time: datetime
    status: str