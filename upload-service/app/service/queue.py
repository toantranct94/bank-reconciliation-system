import asyncio
import logging
from typing import Callable

from aio_pika import Message, connect
from aiormq import AMQPConnectionError
from app.core.config import settings
from app.core.singleton import singleton

logging.basicConfig(level=logging.INFO)


@singleton
class QueueService():
    def __init__(self):
        self.amqp_url = settings.amqp_url
        self.connection = None
        self.channel = None
        self.retry_attempts = 10
        self.retry_delay = 5

    async def connect(self):
        for attempt in range(self.retry_attempts):
            try:
                self.connection = await connect(self.amqp_url)
                break
            except AMQPConnectionError:
                logging.error(
                    (f"Connection attempt {attempt + 1} failed."
                        f"Retrying in {self.retry_delay} seconds..."))
                await asyncio.sleep(self.retry_delay)
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
