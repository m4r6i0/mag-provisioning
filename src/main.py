from fastapi import FastAPI, Request
from starlette.middleware import Middleware
from starlette.middleware.base import BaseHTTPMiddleware
from sqlalchemy.orm import Session

from src.controllers.provision_request_controller import ProvisionRequestController
from src.controllers.audit_log_controller import AuditLogController
from src.controllers.resource_controller import ResourceController
from src.controllers.template_definition_controller import TemplateDefinitionController
from src.controllers.execution_log_controller import ExecutionLogController
from src.infrastructure.database import SessionLocal
from src.interceptors.base_interceptor import ExceptionMiddleware

app = FastAPI(
    middleware=[
        Middleware(ExceptionMiddleware)
    ]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = get_db

app.include_router(ProvisionRequestController(db_dependency).router)
app.include_router(AuditLogController(db_dependency).router)
app.include_router(ResourceController(db_dependency).router)
app.include_router(TemplateDefinitionController(db_dependency).router)
app.include_router(ExecutionLogController(db_dependency).router)