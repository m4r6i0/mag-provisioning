import os
from typing import Optional

class Config:
    def __init__(self):
        pass

    @staticmethod
    def get_env_variable(name: str, default: Optional[str] = None) -> str:
        value = os.environ.get(name)
        if value is None:
            if default is not None:
                return default
            raise ValueError(f"Environment variable '{name}' not found.")
        return value

class RabbitMQConfig(Config):
    def __init__(self):
        super().__init__()
        self.host = self.get_env_variable("RABBITMQ_HOST")
        self.port = int(self.get_env_variable("RABBITMQ_PORT"))
        self.user = self.get_env_variable("RABBITMQ_USER")
        self.password = self.get_env_variable("RABBITMQ_PASSWORD")
        self.queue = self.get_env_variable("RABBITMQ_QUEUE")