import json
import unittest
from fastapi.testclient import TestClient
import logging
from uuid import uuid4
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from src.main import app
from src.infrastructure.database import Base
from src.config.settings import PostgresSettings
from src.repositories.user_repository import UserRepository
from src.entities.user import User
from src.entities.template_definition import TemplateDefinition
from src.repositories.template_definition_repository import TemplateDefinitionRepository
from src.entities.provision_request import ProvisionRequest
from src.repositories.provision_request_repository import ProvisionRequestRepository
from src.entities.audit_log import AuditLog
from src.repositories.audit_log_repository import AuditLogRepository
from src.entities.resource import Resource
from src.repositories.resource_repository import ResourceRepository
from src.entities.worker import Worker
from src.repositories.worker_repository import WorkerRepository
from src.entities.execution_log import ExecutionLog
from src.repositories.execution_log_repository import ExecutionLogRepository




class TestAPI(unittest.TestCase):
    def setUp(self):
        self.settings = PostgresSettings()
        self.engine = create_engine(self.settings.database_url)
        Base.metadata.create_all(bind=self.engine)
        SessionLocal = sessionmaker(
            autocommit=False, autoflush=False, bind=self.engine
        )
        self.db = SessionLocal()
        self.client = TestClient(app)
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    def tearDown(self):
        Base.metadata.drop_all(bind=self.engine)
        self.db.close()

    def test_get_provision_requests(self):
        self.logger.info("test_get_provision_requests started")
        # create a user
        user_repo = UserRepository(self.db)
        user = User(uuid=str(uuid4()), name="User test")
        user_repo.create(user)
        self.db.commit()
        response = self.client.get("/v1/provision-requests")
        self.assertEqual(response.status_code, 200)
        self.logger.info("test_get_provision_requests finished")
        # Add more assertions based on expected response data

    def test_get_provision_requests_with_data(self):
        self.logger.info("test_get_provision_requests_with_data started")
        # Create a user
        user_repo = UserRepository(self.db)
        user = User(uuid=str(uuid4()), name="User test")
        user_repo.create(user)
        self.db.commit()
        # Create a provision request
        provision_request_repo = ProvisionRequestRepository(self.db)
        provision_request = ProvisionRequest(
            user_id=user.uuid,
            request_time="2025-04-09T13:00:00Z",
            status="pending",
            priority=1,
            resource_type="vm-ubuntu-lts",
            parameters={},
            worker_id="worker-az01",
        )
        provision_request_repo.create(provision_request)
        self.db.commit()
        response = self.client.get("/v1/provision-requests")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.json()) > 0)
        self.logger.info("test_get_provision_requests_with_data finished")

    def test_get_provision_requests_by_id(self):
        self.logger.info("test_get_provision_requests_by_id started")
        # Create a user
        user_repo = UserRepository(self.db)
        user = User(uuid=str(uuid4()), name="User test")
        user_repo.create(user)
        self.db.commit()
        # Create a provision request
        provision_request_repo = ProvisionRequestRepository(self.db)
        provision_request = ProvisionRequest(uuid=str(uuid4()), user_id=user.uuid, request_time="2025-04-09T13:00:00Z", status="pending", priority=1, resource_type="vm-ubuntu-lts", parameters={}, worker_id="worker-az01")
        provision_request_repo.create(provision_request)
        self.db.commit()
        response = self.client.get(f"/v1/provision-requests/{provision_request.uuid}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["uuid"], str(provision_request.uuid))
        self.logger.info("test_get_provision_requests_by_id finished")

    def test_create_provision_request(self):
        self.logger.info("test_create_provision_request started")
        # Create a user
        user_repo = UserRepository(self.db)
        user = User(uuid=str(uuid4()), name="User test")
        user_repo.create(user)
        self.db.commit()
        # Create a template definition
        template_definition_repo = TemplateDefinitionRepository(self.db)
        template_definition = TemplateDefinition(uuid="vm-ubuntu-lts", name="Virtual Machine", description="Compute", template_body="Provisionamento de máquina virtual Ubuntu LTS 20.04")
        template_definition_repo.create(template_definition)
        self.db.commit()
        # Create a worker
        worker_repo = WorkerRepository(self.db)
        worker = Worker(uuid="worker-az01", ip_address="10.10.1.42")
        worker_repo.create(worker)
        self.db.commit()
        payload = {
            "user_id": user.uuid,
            "request_time": "2025-04-09T13:00:00Z",
            "status": "pending",
            "priority": 1,
            "resource_type": template_definition.uuid,
            "parameters": {},
            "worker_id": worker.uuid
        }
        response = self.client.post("/v1/provision-requests", json=payload)
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertTrue("uuid" in response_data)
        self.assertEqual(response_data["user_id"], str(user.uuid))
        self.assertEqual(response_data["status"], "pending")
        self.logger.info("test_create_provision_request finished")

    def test_create_provision_request_with_invalid_data(self):
        self.logger.info("test_create_provision_request_with_invalid_data started")
        payload = {
            "invalid_field": "invalid_value"
        }
        response = self.client.post("/v1/provision-requests", json=payload)
        self.assertEqual(response.status_code, 422)
        self.logger.info("test_create_provision_request_with_invalid_data finished")

    def test_update_provision_request(self):
        self.logger.info("test_update_provision_request started")
        # Create a user
        user_repo = UserRepository(self.db)
        user = User(uuid=str(uuid4()), name="User test")
        user_repo.create(user)
        self.db.commit()
        # Create a provision request
        provision_request_repo = ProvisionRequestRepository(self.db)
        provision_request = ProvisionRequest(uuid=str(uuid4()), user_id=user.uuid, request_time="2025-04-09T13:00:00Z", status="pending", priority=1, resource_type="vm-ubuntu-lts", parameters={}, worker_id="worker-az01")
        provision_request_repo.create(provision_request)
        self.db.commit()
        # Update the provision request
        payload = {
            "status": "completed",
            "priority": 2
        }
        response = self.client.put(f"/v1/provision-requests/{provision_request.uuid}", json=payload)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "completed")
        self.assertEqual(response.json()["priority"], 2)
        self.logger.info("test_update_provision_request finished")

    def test_get_audit_logs(self):
        self.logger.info("test_get_audit_logs started")
        response = self.client.get("/v1/audit-logs")
        self.assertEqual(response.status_code, 200)
        self.logger.info("test_get_audit_logs finished")

    def test_get_resources(self):
        self.logger.info("test_get_audit_logs_with_data started")
        audit_log_repo = AuditLogRepository(self.db)
        audit_log = AuditLog(uuid=str(uuid4()), request_id=str(uuid4()), event_name="Test event", data="{}")
        audit_log_repo.create(audit_log)
        self.db.commit()
        response = self.client.get("/v1/audit-logs")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.json()) > 0)
        self.logger.info("test_get_audit_logs_with_data finished")

    def test_get_audit_logs_by_id(self):
        self.logger.info("test_get_audit_logs_by_id started")
        audit_log_repo = AuditLogRepository(self.db)
        audit_log = AuditLog(uuid=str(uuid4()), request_id=str(uuid4()), event_name="Test event", data="{}")
        audit_log_repo.create(audit_log)
        self.db.commit()
        response = self.client.get(f"/v1/audit-logs/{audit_log.uuid}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["uuid"], str(audit_log.uuid))
        self.logger.info("test_get_resources started")
        response = self.client.get("/v1/resources")
        self.logger.info("test_get_audit_logs_by_id finished")
        self.assertEqual(response.status_code, 200)
        self.logger.info("test_get_resources finished")
        resource_repo = ResourceRepository(self.db)
        resource = Resource(uuid=str(uuid4()), request_id=str(uuid4()), resource_type="vm-ubuntu-lts", resource_name="vm-dev-01", cloud_provider="AZURE", status="pending")
        resource_repo.create(resource)
        self.db.commit()
        response = self.client.get("/v1/resources")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.json()) > 0)
        self.logger.info("test_get_resources_with_data finished")

    def test_get_resources_by_id(self):
        self.logger.info("test_get_resources_by_id started")
        resource_repo = ResourceRepository(self.db)
        resource = Resource(uuid=str(uuid4()), request_id=str(uuid4()), resource_type="vm-ubuntu-lts", resource_name="vm-dev-01", cloud_provider="AZURE", status="pending")
        resource_repo.create(resource)
        self.db.commit()
        response = self.client.get(f"/v1/resources/{resource.uuid}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["uuid"], str(resource.uuid))
        self.logger.info("test_get_resources_by_id finished")


    def test_create_template_definitions(self):
        self.logger.info("test_create_template_definitions started")
        template_definition_repo = TemplateDefinitionRepository(self.db)
        template_definition = TemplateDefinition(
        payload = {
            "uuid": "vm-ubuntu-lts",
            "name": "Virtual Machine",
            "description": "Compute",
            "template_body": "Provisionamento de máquina virtual Ubuntu LTS 20.04"
        }
        response = self.client.post("/v1/template-definitions", json=payload)
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertTrue("uuid" in response_data)
        self.assertEqual(response_data["name"], "Virtual Machine")
        self.logger.info("test_create_template_definitions finished")

    def test_create_template_definitions_with_invalid_data(self):
        self.logger.info("test_create_template_definitions_with_invalid_data started")
        payload = {
            "invalid_field": "invalid_value"
        }
        response = self.client.post("/v1/template-definitions", json=payload)
        self.assertEqual(response.status_code, 422)
        self.logger.info("test_create_template_definitions_with_invalid_data finished")

    def test_get_template_definitions_with_data(self):
        self.logger.info("test_get_template_definitions_with_data started")
        template_definition_repo = TemplateDefinitionRepository(self.db)
        template_definition = TemplateDefinition(uuid="vm-ubuntu-lts", name="Virtual Machine", description="Compute", template_body="Provisionamento de máquina virtual Ubuntu LTS 20.04")
        template_definition_repo.create(template_definition)
        self.db.commit()
        response = self.client.get("/v1/template-definitions")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.json()) > 0)
        self.logger.info("test_get_template_definitions_with_data finished")

    def test_get_template_definitions_by_id(self):
        self.logger.info("test_get_template_definitions_by_id started")
        template_definition_repo = TemplateDefinitionRepository(self.db)
        template_definition = TemplateDefinition(uuid="vm-ubuntu-lts", name="Virtual Machine", description="Compute", template_body="Provisionamento de máquina virtual Ubuntu LTS 20.04")
        template_definition_repo.create(template_definition)
        self.db.commit()
        response = self.client.get(f"/v1/template-definitions/{template_definition.uuid}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["uuid"], str(template_definition.uuid))
        self.logger.info("test_get_template_definitions_by_id finished")

    def test_update_audit_log(self):
        self.logger.info("test_update_audit_log started")
        audit_log_repo = AuditLogRepository(self.db)
        audit_log = AuditLog(uuid=str(uuid4()), request_id=str(uuid4()), event_name="Test event", data="{}")
        audit_log_repo.create(audit_log)
        self.db.commit()
        # Update the audit log
        payload = {
            "event_name": "Updated Test event",
            "data": "{updated}"
        }
        response = self.client.put(f"/v1/audit-logs/{audit_log.uuid}", json=payload)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["event_name"], "Updated Test event")
        self.assertEqual(response.json()["data"], "{updated}")
        self.logger.info("test_update_audit_log finished")

    def test_update_resource(self):
        self.logger.info("test_update_resource started")
        resource_repo = ResourceRepository(self.db)
        resource = Resource(uuid=str(uuid4()), request_id=str(uuid4()), resource_type="vm-ubuntu-lts", resource_name="vm-dev-01", cloud_provider="AZURE", status="pending")
        resource_repo.create(resource)
        self.db.commit()
        # Update the resource
        payload = {
            "resource_name": "vm-dev-02",
            "status": "active"
        }
    def test_get_execution_logs(self):

    def test_update_template_definition(self):
        self.logger.info("test_update_template_definition started")
        template_definition_repo = TemplateDefinitionRepository(self.db)
        template_definition = TemplateDefinition(uuid="vm-ubuntu-lts", name="Virtual Machine", description="Compute", template_body="Provisionamento de máquina virtual Ubuntu LTS 20.04")
        template_definition_repo.create(template_definition)
        self.db.commit()
        # Update the template definition
        payload = {
            "name": "Updated Virtual Machine",
            "description": "Updated Compute"
        }
        response = self.client.put(f"/v1/template-definitions/{template_definition.uuid}", json=payload)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["name"], "Updated Virtual Machine")
        self.assertEqual(response.json()["description"], "Updated Compute")
        self.logger.info("test_update_template_definition finished")
    def test_get_execution_logs(self):
        self.logger.info("test_get_execution_logs started")
        response = self.client.get("/v1/execution-logs")
        self.assertEqual(response.status_code, 200)
        self.logger.info("test_get_execution_logs finished")

    def test_get_execution_logs_with_data(self):
        self.logger.info("test_get_execution_logs_with_data started")
        execution_log_repo = ExecutionLogRepository(self.db)
        execution_log = ExecutionLog(uuid=str(uuid4()), request_id=str(uuid4()), log="Test log")
        execution_log_repo.create(execution_log)
        self.db.commit()
        response = self.client.get("/v1/execution-logs")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.json()) > 0)
        self.logger.info("test_get_execution_logs_with_data finished")

    def test_get_execution_logs_by_id(self):
        self.logger.info("test_get_execution_logs_by_id started")
        execution_log_repo = ExecutionLogRepository(self.db)
        execution_log = ExecutionLog(uuid=str(uuid4()), request_id=str(uuid4()), log="Test log")
        execution_log_repo.create(execution_log)
        self.db.commit()
        response = self.client.get(f"/v1/execution-logs/{execution_log.uuid}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["uuid"], str(execution_log.uuid))
        self.logger.info("test_get_execution_logs_by_id finished")
    def test_update_execution_log(self):
        self.logger.info("test_update_execution_log started")
        execution_log_repo = ExecutionLogRepository(self.db)
        execution_log = ExecutionLog(uuid=str(uuid4()), request_id=str(uuid4()), log="Test log")
        execution_log_repo.create(execution_log)
        self.db.commit()
        # Update the execution log
        payload = {
            "log": "Updated Test log"
        }
        response = self.client.put(f"/v1/execution-logs/{execution_log.uuid}", json=payload)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["log"], "Updated Test log")
        self.logger.info("test_update_execution_log finished")

    def test_delete_provision_request(self):
        self.logger.info("test_delete_provision_request started")
        # Create a user
        user_repo = UserRepository(self.db)
        user = User(uuid=str(uuid4()), name="User test")
        user_repo.create(user)
        self.db.commit()
        # Create a provision request
        provision_request_repo = ProvisionRequestRepository(self.db)
        provision_request = ProvisionRequest(uuid=str(uuid4()), user_id=user.uuid, request_time="2025-04-09T13:00:00Z", status="pending", priority=1, resource_type="vm-ubuntu-lts", parameters={}, worker_id="worker-az01")
        provision_request_repo.create(provision_request)
        self.db.commit()
        # Delete the provision request
        response = self.client.delete(f"/v1/provision-requests/{provision_request.uuid}")
        self.assertEqual(response.status_code, 200)
        self.logger.info("test_delete_provision_request finished")

    def test_delete_audit_log(self):
        self.logger.info("test_delete_audit_log started")
        audit_log_repo = AuditLogRepository(self.db)
        audit_log = AuditLog(uuid=str(uuid4()), request_id=str(uuid4()), event_name="Test event", data="{}")
        audit_log_repo.create(audit_log)
        self.db.commit()
        # Delete the audit log
        response = self.client.delete(f"/v1/audit-logs/{audit_log.uuid}")
        self.assertEqual(response.status_code, 200)
        self.logger.info("test_delete_audit_log finished")

    def test_delete_resource(self):
        self.logger.info("test_delete_resource started")
        resource_repo = ResourceRepository(self.db)
        resource = Resource(uuid=str(uuid4()), request_id=str(uuid4()), resource_type="vm-ubuntu-lts", resource_name="vm-dev-01", cloud_provider="AZURE", status="pending")
        resource_repo.create(resource)
        self.db.commit()
        # Delete the resource
        response = self.client.delete(f"/v1/resources/{resource.uuid}")
        self.assertEqual(response.status_code, 200)
        self.logger.info("test_delete_resource finished")

    def test_delete_template_definition(self):
        self.logger.info("test_delete_template_definition started")
        template_definition_repo = TemplateDefinitionRepository(self.db)
        template_definition = TemplateDefinition(uuid="vm-ubuntu-lts", name="Virtual Machine", description="Compute", template_body="Provisionamento de máquina virtual Ubuntu LTS 20.04")
        template_definition_repo.create(template_definition)
        self.db.commit()
        # Delete the template definition
        response = self.client.delete(f"/v1/template-definitions/{template_definition.uuid}")
        self.assertEqual(response.status_code, 200)
        self.logger.info("test_delete_template_definition finished")

    def test_delete_execution_log(self):
        self.logger.info("test_delete_execution_log started")
        execution_log_repo = ExecutionLogRepository(self.db)
        execution_log = ExecutionLog(uuid=str(uuid4()), request_id=str(uuid4()), log="Test log")
        execution_log_repo.create(execution_log)
        self.db.commit()
        # Delete the execution log
        response = self.client.delete(f"/v1/execution-logs/{execution_log.uuid}")
        self.assertEqual(response.status_code, 200)
        self.logger.info("test_delete_execution_log finished")
    def test_get_template_definitions(self):
        self.logger.info("test_get_template_definitions started")
        response = self.client.get("/v1/template-definitions")
        self.assertEqual(response.status_code, 200)
        self.logger.info("test_get_template_definitions finished")