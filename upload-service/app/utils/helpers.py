import hashlib
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


async def is_upload_file_valid(file: UploadFile, sumcheck: str) -> bool:
    md5, file_size = await calculate_md5_filesize(file)

    if not is_content_file_valid(file):
        return False
    if not is_sumcheck_valid(md5, sumcheck):
        return False
    if not is_file_size_valid(file_size):
        return False
    return True


async def calculate_md5_filesize(file: UploadFile):
    # Calculate the MD5 hash of the file
    md5_hash = hashlib.md5()
    file_size = 0
    while chunk := await file.read(4096):
        md5_hash.update(chunk)
        file_size += len(chunk)
    await file.seek(0)

    return md5_hash.hexdigest(), file_size


def is_content_file_valid(file: UploadFile):
    file_extension = get_extension(file)
    if file_extension not in settings.ALLOWED_EXTENSIONS:
        return False
    return True


def is_file_size_valid(file_size: int):
    # file.file.seek(0, 2)
    # file_size = file.file.tell()
    # # move the cursor back to the beginning
    # await file.seek(0)
    # logging.info(f"File size: {file_size}")
    return file_size <= settings.MAX_FILE_SIZE_BYTES


def is_sumcheck_valid(md5_hash: str, sumcheck: str) -> bool:
    # Calculate the MD5 hash of the file
    return md5_hash == sumcheck
