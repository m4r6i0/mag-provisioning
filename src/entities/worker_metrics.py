import uuid
from sqlalchemy import Column, Integer, Numeric, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from src.infrastructure.database import Base


class WorkerMetrics(Base):
    __tablename__ = "worker_metrics"

    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    worker_id = Column(UUID(as_uuid=True), ForeignKey("workers.uuid"))
    cpu_usage = Column(Numeric)
    memory_usage = Column(Numeric)
    tasks_processed = Column(Integer)
    metric_time = Column(DateTime)

    worker = relationship("Worker", back_populates="metrics")