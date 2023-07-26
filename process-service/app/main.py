import asyncio
# import json
import logging
import os

from aio_pika import IncomingMessage
from services.db import CsvToPostgresImporter
from services.queue import QueueService

queue_service = QueueService()

logging.basicConfig(level=logging.INFO)
importer = CsvToPostgresImporter()


async def on_message(message: IncomingMessage):
    file_path = message.body.decode("utf-8")
    file_path = file_path.replace("././", "../")
    logging.info(f"Received message: {file_path}")
    if os.path.exists(file_path):
        logging.info(f"Importing data from {file_path}")
        importer.set_file(file_path)
        importer.import_data()
    else:
        logging.error("File not found")


async def main():
    await queue_service.connect()
    queue = await queue_service.channel.declare_queue("pgdb", exclusive=True)
    await queue.consume(on_message)


if __name__ == "__main__":
    logging.info("Start listening...")
    loop = asyncio.get_event_loop()
    loop.create_task(main())
    loop.run_forever()
