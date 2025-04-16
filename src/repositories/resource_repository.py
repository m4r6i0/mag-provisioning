from sqlalchemy.orm import Session
from src.entities.resource import Resource
from uuid import UUID


class ResourceRepository:
    def __init__(self, session: Session):
        self.session = session

    def find_by_id(self, uuid: UUID) -> Resource | None:
        return self.session.query(Resource).filter(Resource.uuid == uuid).first()

    def find_all(self) -> list[Resource]:
        return self.session.query(Resource).all()

    def create(self, resource: Resource) -> Resource:
        self.session.add(resource)
        self.session.commit()
        self.session.refresh(resource)
        return resource

    def update(self, uuid: UUID, resource: Resource) -> Resource | None:
        existing_resource = self.find_by_id(uuid)
        if existing_resource:
            for key, value in resource.__dict__.items():
                if key != "uuid" and hasattr(existing_resource, key):
                    setattr(existing_resource, key, value)
            self.session.commit()
            self.session.refresh(existing_resource)
            return existing_resource
        return None

    def delete(self, uuid: UUID) -> bool:
        resource = self.find_by_id(uuid)
        if resource:
            self.session.delete(resource)
            self.session.commit()
            return True
        return False