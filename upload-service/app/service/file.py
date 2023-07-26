import os
from uuid import uuid4

from app.core.config import settings
from app.models.schemas.files import Folder
# from worker.tasks import import_csv_to_postgres
from app.service.queue import QueueService
from fastapi import UploadFile

queue_service = QueueService()


def create_folder(name: str = None) -> Folder:
    if not name:
        name = str(uuid4())

    os.makedirs(f"{settings.UPLOAD_FOLDER}{name}")

    folder = {
        "folder": name
    }

    return Folder(**folder)


async def save_file(file_path: str, file: UploadFile):
    with open(file_path, "wb") as f:
        while True:
            data = await file.read(settings.MAX_READ_CHUNK_BYTES)
            if not data:
                break
            f.write(data)
    # import_csv_to_postgres.delay(file_path)
    await queue_service.publish_message(file_path)
