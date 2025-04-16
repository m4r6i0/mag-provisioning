from sqlalchemy.orm import Session
from src.entities.provision_request import ProvisionRequest
from uuid import UUID

class ProvisionRequestRepository:
    def __init__(self, session: Session):
        self.session = session

    def find_by_id(self, uuid: UUID) -> ProvisionRequest:
        return self.session.query(ProvisionRequest).filter(ProvisionRequest.uuid == uuid).first()

    def find_all(self) -> list[ProvisionRequest]:
        return self.session.query(ProvisionRequest).all()

    def create(self, provision_request: ProvisionRequest) -> ProvisionRequest:
        self.session.add(provision_request)
        self.session.commit()
        self.session.refresh(provision_request)
        return provision_request

    def update(self, provision_request: ProvisionRequest) -> ProvisionRequest:
        self.session.commit()
        self.session.refresh(provision_request)
        return provision_request

    def delete(self, uuid: UUID):
        provision_request = self.find_by_id(uuid)
        if provision_request:
            self.session.delete(provision_request)
            self.session.commit()