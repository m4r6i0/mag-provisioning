from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class WorkerMetricsDTO(BaseModel):
    uuid: UUID
    worker_id: UUID
    cpu_usage: float
    memory_usage: float
    tasks_processed: int
    metric_time: datetime