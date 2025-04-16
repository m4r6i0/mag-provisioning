from sqlalchemy import Column, String, ForeignKey, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
import uuid
from datetime import datetime

Base = declarative_base()

class ResourceTag(Base):
    __tablename__ = 'resource_tags'

    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    resource_id = Column(UUID(as_uuid=True), ForeignKey('resources.uuid'), nullable=False)
    tag_key = Column(String, nullable=False)
    tag_value = Column(String, nullable=False)