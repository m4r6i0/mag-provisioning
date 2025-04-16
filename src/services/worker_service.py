from src.entities.worker import Worker
from src.repositories.worker_repository import WorkerRepository

class WorkerService:

    def __init__(self, worker_repository: WorkerRepository):
        self.worker_repository = worker_repository

    def create(self, worker: Worker):
        return self.worker_repository.create(worker)