import uuid
from sqlalchemy import Column, String, DateTime, Enum, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from src.infrastructure.database import Base
import enum

class ProvisionRequestStatus(enum.Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"

class ProvisionRequest(Base):
    __tablename__ = "provision_requests"

    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.uuid"), nullable=False)
    request_time = Column(DateTime, nullable=False)
    status = Column(Enum(ProvisionRequestStatus), nullable=False)
    priority = Column(Integer, nullable=False)
    resource_type = Column(String, nullable=False)
    parameters = Column(JSONB, nullable=False)
    worker_id = Column(UUID(as_uuid=True), ForeignKey("workers.uuid"))
    last_update = Column(DateTime, nullable=False)

    user = relationship("User", back_populates="provision_requests")
    worker = relationship("Worker", back_populates="provision_requests")