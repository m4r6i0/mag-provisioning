from sqlalchemy.orm import Mapped, mapped_column
from src.infrastructure.database import Base
from uuid import UUID
from sqlalchemy.sql import func
from datetime import datetime
from enum import Enum
class UserRole(Enum):
    ADMIN = "admin"
    USER = "user"

class User(Base):
    __tablename__ = "users"

    uuid: Mapped[UUID] = mapped_column(primary_key=True)
    name: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    role: Mapped[UserRole]
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())