from sqlalchemy.orm import Session
from src.entities.resource_dependency import ResourceDependency
from uuid import UUID


class ResourceDependencyRepository:
    def __init__(self, session: Session):
        self.session = session

    def find_by_id(self, uuid: UUID) -> ResourceDependency:
        return self.session.query(ResourceDependency).filter(ResourceDependency.uuid == uuid).first()

    def find_all(self) -> list[ResourceDependency]:
        return self.session.query(ResourceDependency).all()

    def create(self, resource_dependency: ResourceDependency) -> ResourceDependency:
        self.session.add(resource_dependency)
        self.session.commit()
        self.session.refresh(resource_dependency)
        return resource_dependency

    def update(self, resource_dependency: ResourceDependency) -> ResourceDependency:
        self.session.commit()
        self.session.refresh(resource_dependency)
        return resource_dependency

    def delete(self, uuid: UUID):
        resource_dependency = self.find_by_id(uuid)
        if resource_dependency:
            self.session.delete(resource_dependency)
            self.session.commit()