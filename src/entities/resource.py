import uuid
from sqlalchemy import Column, String, DateTime, Enum, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from src.infrastructure.database import Base
import enum

class ResourceStatus(enum.Enum):
    active = "active"
    terminated = "terminated"

class Resource(Base):
    __tablename__ = "resources"

    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    request_id = Column(UUID(as_uuid=True), ForeignKey("provision_requests.uuid"), nullable=False)
    resource_type = Column(String, nullable=False)
    resource_name = Column(String, nullable=False)
    cloud_provider = Column(String, nullable=False)
    status = Column(Enum(ResourceStatus), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())