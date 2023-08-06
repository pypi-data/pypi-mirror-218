from typing import Any
from abc import ABC, abstractmethod

import json
from pika import BlockingConnection

from .types import Subjects

class AbstractPublisher(ABC):
    @property
    @abstractmethod
    def subject(self) -> Subjects | str:
        raise NotImplementedError()

    @abstractmethod
    def publish(self, data: Any):
        pass

    def on_publish(self, data: Any):
        self.channel.basic_publish(exchange='', routing_key=self.subject, body=json.dumps(data).encode('utf-8'))

    def __init__(self, connection: BlockingConnection):
        self.channel = connection.channel()  # Start a channel.
        self.channel.queue_declare(queue=self.subject)  # Declare a queue.
