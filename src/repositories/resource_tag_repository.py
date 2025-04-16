from sqlalchemy.orm import Session
from src.entities.resource_tag import ResourceTag
from uuid import UUID

class ResourceTagRepository:
    def __init__(self, session: Session):
        self.session = session

    def find_by_id(self, uuid: UUID) -> ResourceTag:
        return self.session.query(ResourceTag).filter(ResourceTag.uuid == uuid).first()

    def find_all(self) -> list[ResourceTag]:
        return self.session.query(ResourceTag).all()

    def create(self, resource_tag: ResourceTag) -> ResourceTag:
        self.session.add(resource_tag)
        self.session.commit()
        self.session.refresh(resource_tag)
        return resource_tag

    def update(self, resource_tag: ResourceTag) -> ResourceTag:
        self.session.commit()
        self.session.refresh(resource_tag)
        return resource_tag

    def delete(self, resource_tag: ResourceTag):
        self.session.delete(resource_tag)
        self.session.commit()