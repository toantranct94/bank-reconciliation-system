import asyncio
# import json
import logging
import os

from aio_pika import IncomingMessage
from services.db import ImporterFactory
from services.queue import QueueService

queue_service = QueueService()

logging.basicConfig(level=logging.INFO)


async def on_message(message: IncomingMessage):
    file_path = message.body.decode("utf-8")
    file_path = file_path.replace("././", "../")
    logging.info(f"Received message: {file_path}")

    if not os.path.exists(file_path):
        logging.error("File not found")
        return

    logging.info(f"Importing data from {file_path}")
    importer = ImporterFactory(file_path)
    importer.import_data()


async def main():
    await queue_service.connect()
    queue = await queue_service.channel.declare_queue("pgdb", exclusive=True)
    await queue.consume(on_message)


if __name__ == "__main__":
    logging.info("Start listening...")
    loop = asyncio.get_event_loop()
    loop.create_task(main())
    loop.run_forever()
