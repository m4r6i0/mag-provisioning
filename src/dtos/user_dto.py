from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class UserDTO(BaseModel):
    uuid: UUID
    name: str
    email: str
    role: str
    created_at: datetime