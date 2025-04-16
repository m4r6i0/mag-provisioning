from sqlalchemy.orm import Session
from src.entities.worker_metrics import WorkerMetrics
from uuid import UUID

class WorkerMetricsRepository:
    def __init__(self, session: Session):
        self.session = session

    def find_by_id(self, id: UUID) -> WorkerMetrics:
        return self.session.query(WorkerMetrics).filter(WorkerMetrics.uuid == id).first()

    def find_all(self) -> list[WorkerMetrics]:
        return self.session.query(WorkerMetrics).all()

    def create(self, worker_metrics: WorkerMetrics) -> WorkerMetrics:
        self.session.add(worker_metrics)
        self.session.commit()
        self.session.refresh(worker_metrics)
        return worker_metrics

    def update(self, worker_metrics: WorkerMetrics) -> WorkerMetrics:
        self.session.commit()
        self.session.refresh(worker_metrics)
        return worker_metrics

    def delete(self, id: UUID):
        worker_metrics = self.find_by_id(id)
        if worker_metrics:
            self.session.delete(worker_metrics)
            self.session.commit()