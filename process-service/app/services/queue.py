import logging
from typing import Callable

from aio_pika import Message, connect
from core.config import settings
from core.singleton import singleton

logger = logging.getLogger(__name__)


@singleton
class QueueService():
    def __init__(self):
        self.amqp_url = settings.amqp_url
        self.connection = None
        self.channel = None

    async def connect(self):
        self.connection = await connect(self.amqp_url)
        self.channel = await self.connection.channel()
        # take 10 messages in advance
        await self.channel.set_qos(prefetch_count=10)
        logger.info("Connected to RabbitMQ")

    async def close(self):
        await self.connection.close()
        logger.info("Disconnected from RabbitMQ")

    async def publish_message(self, message: str, routing_key: str = "pgdb"):
        await self.channel.default_exchange.publish(
            Message(message.encode()),
            routing_key=routing_key
        )
        logger.info("Message published")

    async def consume_messages(self, queue_name: str, callback: Callable):
        queue = await self.channel.declare_queue(queue_name)
        await queue.consume(callback)
        logger.info("Message consumed")
