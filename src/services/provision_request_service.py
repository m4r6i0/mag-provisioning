from typing import List
from sqlalchemy.orm import Session
from src.entities.provision_request import ProvisionRequest
from src.repositories.provision_request_repository import ProvisionRequestRepository
import pika
import json
import uuid

class ProvisionRequestService:
    def __init__(self, session: Session, repository: ProvisionRequestRepository):
        self.session = session
        self.repository = repository

    def find_all(self) -> List[ProvisionRequest]:
        return self.repository.find_all()

    def find_by_id(self, id: uuid.UUID) -> ProvisionRequest:
        return self.repository.find_by_id(id)

    def listen_rabbitmq(self):
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        channel = connection.channel()

        channel.queue_declare(queue='resource-provisioning')

        def callback(ch, method, properties, body):
            print(f" [x] Received {body}")
            try:
                message_data = json.loads(body)
                provision_request = ProvisionRequest(**message_data)
                self.repository.create(provision_request)
            except Exception as e:
                print(f"Error processing message: {e}")

        channel.basic_consume(queue='resource-provisioning', on_message_callback=callback, auto_ack=True)

        print(' [*] Waiting for messages. To exit press CTRL+C')
        channel.start_consuming()