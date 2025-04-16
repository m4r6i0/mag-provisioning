import datetime
import uuid

from sqlalchemy import DateTime, Enum, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column

from src.infrastructure.database import Base




class ExecutionLog(Base):
    __tablename__ = "execution_logs"

    uuid: Mapped[str] = mapped_column(primary_key=True, default=uuid.uuid4)
    request_id: Mapped[str] = mapped_column(ForeignKey("provision_requests.uuid"))
    worker_id: Mapped[str] = mapped_column(ForeignKey("workers.uuid"))
    message: Mapped[str] = mapped_column(Text)
    log_time: Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.datetime.utcnow)
    status: Mapped[str] = mapped_column(Enum("info", "warning", "error", name="log_status"))