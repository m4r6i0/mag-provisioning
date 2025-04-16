from fastapi import FastAPI
from starlette.middleware import Middleware
from src.interceptors.base_interceptor import ExceptionInterceptor
from src.controllers.provision_request_controller import ProvisionRequestController
from src.controllers.audit_log_controller import AuditLogController
from src.controllers.resource_controller import ResourceController
from src.controllers.template_definition_controller import TemplateDefinitionController
from src.controllers.execution_log_controller import ExecutionLogController
from src.infrastructure.database import get_db, engine
from src.services.provision_request_service import ProvisionRequestService
from src.repositories.provision_request_repository import ProvisionRequestRepository
from sqlalchemy.orm import Session
import threading

app = FastAPI(middleware=[Middleware(ExceptionInterceptor)])


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
    session = get_session()
    provision_request_repository = ProvisionRequestRepository(session)
    provision_request_service = ProvisionRequestService(
        provision_request_repository, session
    )
    provision_request_service.listen_rabbitmq()


# Run the RabbitMQ consumer in a separate thread
rabbitmq_thread = threading.Thread(target=start_rabbitmq_consumer)
rabbitmq_thread.daemon = True
rabbitmq_thread.start()