from typing import List, Dict
from sqlalchemy.orm import Session
from src.entities.provision_request import ProvisionRequest as ProvisionRequestEntity
from src.repositories.provision_request_repository import ProvisionRequestRepository
from src.entities.user import User
from src.entities.worker import Worker
from src.entities.template_definition import TemplateDefinition
from src.entities.resource import Resource
from src.entities.resource_dependency import ResourceDependency
from src.repositories.user_repository import UserRepository
from src.repositories.worker_repository import WorkerRepository
from src.repositories.template_definition_repository import TemplateDefinitionRepository
from src.repositories.resource_repository import ResourceRepository
from src.repositories.resource_dependency_repository import ResourceDependencyRepository
import pika
import json
import uuid
from src.config.settings import RabbitMQSettings
import logging

logging.basicConfig(level=logging.INFO)

class ProvisionRequestService:
    def __init__(
        self,
        session: Session,
        provision_request_repository: ProvisionRequestRepository,
        user_repository: UserRepository,
        worker_repository: WorkerRepository,
        template_definition_repository: TemplateDefinitionRepository,
        resource_repository: ResourceRepository,
        resource_dependency_repository: ResourceDependencyRepository,
    ):
        self.session = session
        self.provision_request_repository = provision_request_repository
        self.user_repository = user_repository
        self.worker_repository = worker_repository
        self.template_definition_repository = template_definition_repository
        self.resource_repository = resource_repository
        self.resource_dependency_repository = resource_dependency_repository
        self.settings = RabbitMQSettings()

    def find_all(self) -> List[ProvisionRequestEntity]:
        return self.provision_request_repository.find_all()

    def find_by_id(self, id: uuid.UUID) -> ProvisionRequestEntity:
        return self.provision_request_repository.find_by_id(id)

    def listen_rabbitmq(self):
        logging.info("Connecting to RabbitMQ...")
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=self.settings.rabbitmq_host,
                port=self.settings.rabbitmq_port,
                credentials=pika.PlainCredentials(
                    self.settings.rabbitmq_user, self.settings.rabbitmq_password
                ),
            )
        )
        channel = connection.channel()

        channel.queue_declare(queue=self.settings.rabbitmq_queue)

        def callback(ch, method, properties, body):
            logging.info(f" [x] Received message: {body.decode()}")
            try:
                message_data: Dict = json.loads(body.decode())
                with self.session.begin():
                    # User
                    user = self.user_repository.find_by_name(message_data["requested_by"])
                    if not user:
                        logging.info(f"Creating new user: {message_data['requested_by']}")
                        user = User(name=message_data["requested_by"])
                        self.user_repository.create(user)
                    user_id = user.uuid
                    logging.info(f"User ID: {user_id}")
                    # Worker
                    worker = self.worker_repository.find_by_id(message_data["worker"]["id"])
                    if not worker:
                        logging.info(f"Creating new worker: {message_data['worker']['id']}")
                        worker = Worker(uuid=message_data["worker"]["id"], ip_address=message_data["worker"]["ip_address"])
                        self.worker_repository.create(worker)
                    worker_id = worker.uuid
                    logging.info(f"Worker ID: {worker_id}")
                    # Template Definition
                    template_definition = self.template_definition_repository.find_by_id(message_data["resource_type"]["id"])
                    if not template_definition:
                        logging.info(f"Creating new template definition: {message_data['resource_type']['id']}")
                        template_definition = TemplateDefinition(uuid=message_data["resource_type"]["id"], name=message_data["resource_type"]["name"], description=message_data["resource_type"]["category"], template_body=message_data["resource_type"]["description"])
                        self.template_definition_repository.create(template_definition)
                    template_definition_id = template_definition.uuid
                    logging.info(f"Template Definition ID: {template_definition_id}")
                    # Provision Request
                    provision_request = ProvisionRequestEntity(user_id=user_id, request_time=message_data["request_time"], status="pending", priority=message_data["priority"], resource_type=template_definition_id, parameters=message_data["parameters"], worker_id=worker_id)
                    self.provision_request_repository.create(provision_request)
                    logging.info(f"Provision Request created with ID: {provision_request.uuid}")
                    # Resource
                    resource = Resource(request_id=provision_request.uuid, resource_type=template_definition_id, resource_name=message_data["parameters"]["name"], cloud_provider="AZURE", status="pending")
                    self.resource_repository.create(resource)
                    logging.info(f"Resource created with ID: {resource.uuid}")
                    # Dependencies
                    for dependency in message_data["dependencies"]:
                        dep = ResourceDependency(resource_id=resource.uuid, depends_on_id=dependency["resource_id"])
                        self.resource_dependency_repository.create(dep)
                        logging.info(f"Resource dependency created: {dep.uuid}")
            except Exception as e:
                logging.error(f"Error processing message: {e}")

        channel.basic_consume(queue=self.settings.rabbitmq_queue, on_message_callback=callback, auto_ack=True)

        logging.info(" [*] Waiting for messages. To exit press CTRL+C")
        channel.start_consuming()