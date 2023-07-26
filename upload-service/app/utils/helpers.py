import logging
import os
from functools import cache
from uuid import uuid4

from app.core.config import settings
from fastapi import UploadFile

logging.basicConfig(level=logging.INFO)


@cache
def get_extension(file: UploadFile):
    return file.filename.split(".")[-1].lower()


def generate_store_path(file: UploadFile, folder_path: str):
    file_extension = get_extension(file)
    random_filename = f"{str(uuid4())}.{file_extension}"
    file_path = os.path.join(folder_path, random_filename)
    return file_path


def is_content_file_valid(file: UploadFile):
    file_extension = get_extension(file)
    if file_extension not in settings.ALLOWED_EXTENSIONS:
        return False
    return True


async def is_file_size_valid(file: UploadFile):
    file.file.seek(0, 2)
    file_size = file.file.tell()
    # move the cursor back to the beginning
    await file.seek(0)
    logging.info(f"File size: {file_size}")
    return file_size > settings.MAX_FILE_SIZE_BYTES
