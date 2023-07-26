import os
from uuid import uuid4

from fastapi import UploadFile


def get_extension(file: UploadFile):
    return file.filename.split(".")[-1].lower()


def generate_store_path(folder_path: str, file_extension: str):
    random_filename = f"{str(uuid4())}.{file_extension}"
    file_path = os.path.join(folder_path, random_filename)
    return file_path
