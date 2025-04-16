from src.repositories.resource_dependency_repository import ResourceDependencyRepository
from src.entities.resource_dependency import ResourceDependency

class ResourceDependencyService:

    def __init__(self, session, resource_dependency_repository: ResourceDependencyRepository):
        self.session = session
        self.resource_dependency_repository = resource_dependency_repository

    def create(self, resource_dependency: ResourceDependency):
        return self.resource_dependency_repository.create(resource_dependency)