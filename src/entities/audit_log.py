from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from src.infrastructure.database import Base 
from uuid import UUID
from sqlalchemy.sql import func
from datetime import datetime

class AuditLog(Base):
    __tablename__ = "audit_logs"

    uuid: Mapped[UUID] = mapped_column(primary_key=True)
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.uuid"))
    action: Mapped[str]
    entity_type: Mapped[str]
    entity_id: Mapped[UUID] 
    description: Mapped[str]
    timestamp: Mapped[datetime] = mapped_column(server_default=func.now())