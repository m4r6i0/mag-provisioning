from sqlalchemy.orm import Session
from src.entities.worker import Worker
from uuid import UUID


class WorkerRepository:
    def __init__(self, session: Session):
        self.session = session

    def find_by_id(self, worker_id: UUID) -> Worker | None:
        return self.session.query(Worker).filter(Worker.uuid == worker_id).first()

    def find_all(self) -> list[Worker]:
        return self.session.query(Worker).all()

    def create(self, worker: Worker) -> Worker:
        self.session.add(worker)
        self.session.commit()
        self.session.refresh(worker)
        return worker

    def update(self, worker: Worker) -> Worker:
        self.session.commit()
        self.session.refresh(worker)
        return worker

    def delete(self, worker: Worker):
        self.session.delete(worker)
        self.session.commit()