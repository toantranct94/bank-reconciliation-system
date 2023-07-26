import os
from uuid import uuid4

from app.core.config import settings
from app.models.schemas.files import Folder
from app.service.queue import QueueService
from app.utils.helpers import generate_store_path
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


async def save_file(file: UploadFile, folder_path: str) -> None:

    file_path = generate_store_path(file, folder_path)

    with open(file_path, "wb") as f:
        while True:
            data = await file.read(settings.MAX_READ_CHUNK_BYTES)
            if not data:
                break
            f.write(data)

    await queue_service.publish_message(file_path)
