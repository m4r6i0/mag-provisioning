import uuid
from sqlalchemy import Column, String, DateTime, Enum, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
import datetime

Base = declarative_base()


class ExecutionLog(Base):
    __tablename__ = "execution_logs"

    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    request_id = Column(UUID(as_uuid=True), ForeignKey("provision_requests.uuid"))
    worker_id = Column(UUID(as_uuid=True), ForeignKey("workers.uuid"))
    log_message = Column(Text)
    log_time = Column(DateTime, default=datetime.datetime.utcnow)
    status = Column(Enum("info", "warning", "error", name="log_status"))