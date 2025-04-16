import uuid
from sqlalchemy import Column, String, Enum, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
import enum

Base = declarative_base()

class WorkerStatus(enum.Enum):
    active = "active"
    busy = "busy"
    down = "down"

class Worker(Base):
    __tablename__ = "workers"

    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    ip_address = Column(String)
    status = Column(Enum(WorkerStatus))
    last_seen = Column(DateTime)