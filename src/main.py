from fastapi import FastAPI
from starlette.middleware import Middleware
from sqlalchemy.orm import configure_mappers
from src.interceptors.base_interceptor import ExceptionInterceptor
from src.controllers.provision_request_controller import ProvisionRequestController
from src.controllers.audit_log_controller import AuditLogController
from src.controllers.resource_controller import ResourceController
from src.controllers.template_definition_controller import TemplateDefinitionController
from src.controllers.execution_log_controller import ExecutionLogController
from src.infrastructure.database import engine, get_db
from src.services.provision_request_service import ProvisionRequestService
from src.repositories.provision_request_repository import ProvisionRequestRepository
from src.repositories.template_definition_repository import TemplateDefinitionRepository
from src.repositories.resource_repository import ResourceRepository
from src.repositories.resource_dependency_repository import ResourceDependencyRepository
from src.repositories.worker_repository import WorkerRepository
from src.repositories.user_repository import UserRepository
from sqlalchemy.orm import Session
import threading
from src.entities.user import User
from src.entities.worker import Worker
from src.entities.template_definition import TemplateDefinition
from src.entities.resource import Resource
from src.entities.provision_request import ProvisionRequest
from src.entities.resource_dependency import ResourceDependency
from src.entities.execution_log import ExecutionLog
from src.entities.audit_log import AuditLog

app = FastAPI(middleware=[Middleware(ExceptionInterceptor)])




configure_mappers()

def get_session():
    db: Session = next(get_db(engine))
    return db


# Controllers
provision_request_controller = ProvisionRequestController(get_session())
audit_log_controller = AuditLogController(get_session())
resource_controller = ResourceController(get_session())
template_definition_controller = TemplateDefinitionController(get_session())
execution_log_controller = ExecutionLogController(get_session())

app.include_router(provision_request_controller.router)
app.include_router(audit_log_controller.router)
app.include_router(resource_controller.router)
app.include_router(template_definition_controller.router)
app.include_router(execution_log_controller.router)


def start_rabbitmq_consumer():
    db: Session = next(get_db(engine))
    provision_request_repository = ProvisionRequestRepository(db)
    template_definition_repository = TemplateDefinitionRepository(db)
    resource_repository = ResourceRepository(db)
    resource_dependency_repository = ResourceDependencyRepository(db)
    worker_repository = WorkerRepository(db)
    user_repository = UserRepository(db)
    provision_request_service = ProvisionRequestService(
        provision_request_repository,
        template_definition_repository,
        resource_repository,
        resource_dependency_repository,
        worker_repository,
        user_repository,
        db,
    )
    provision_request_service.listen_rabbitmq()


# Run the RabbitMQ consumer in a separate thread
rabbitmq_thread = threading.Thread(target=start_rabbitmq_consumer)
rabbitmq_thread.daemon = True
rabbitmq_thread.start()