from sqlalchemy.orm import Session
from src.entities.resource import Resource
from src.repositories.resource_repository import ResourceRepository
from uuid import UUID

class ResourceService:
    def __init__(self, session: Session):
        self.resource_repository = ResourceRepository(session)

    def find_all(self) -> list[Resource]:
        return self.resource_repository.find_all()

    def find_by_id(self, id: UUID) -> Resource:
        return self.resource_repository.find_by_id(id)