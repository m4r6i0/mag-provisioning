import uuid
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from src.infrastructure.database import Base


class ResourceDependency(Base):
    __tablename__ = "resource_dependencies"

    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    resource_id = Column(UUID(as_uuid=True), ForeignKey("resources.uuid"))
    depends_on_id = Column(UUID(as_uuid=True), ForeignKey("resources.uuid"))

    resource = relationship("Resource", foreign_keys=[resource_id])
    depends_on = relationship("Resource", foreign_keys=[depends_on_id])