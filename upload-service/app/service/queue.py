import logging
from typing import Callable

from aio_pika import Message, connect
from app.core.config import settings
from app.core.singleton import singleton

logging.basicConfig(level=logging.INFO)


@singleton
class QueueService():
    def __init__(self):
        self.amqp_url = settings.amqp_url
        self.connection = None
        self.channel = None

    async def connect(self):
        self.connection = await connect(self.amqp_url)
        self.channel = await self.connection.channel()
        logging.info("Connected to RabbitMQ")

    async def close(self):
        await self.connection.close()
        logging.info("Disconnected from RabbitMQ")

    async def publish_message(self, message: str, routing_key: str = "pgdb"):
        await self.channel.default_exchange.publish(
            Message(message.encode()),
            routing_key=routing_key
        )
        logging.info("Message published")

    async def consume_messages(self, queue_name: str, callback: Callable):
        queue = await self.channel.declare_queue(queue_name)
        await queue.consume(callback)
        logging.info("Message consumed")
