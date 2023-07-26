import logging
import os

from app.core.config import settings
from app.core.verify import verify_token
from app.models.schemas.files import Folder
from app.models.schemas.health import Health
from app.service.file import create_folder, save_file
from app.utils.helpers import generate_store_path, get_extension
from fastapi import (APIRouter, BackgroundTasks, Depends, File, HTTPException,
                     UploadFile, status)
from fastapi.responses import JSONResponse

router = APIRouter()
logging.basicConfig(level=logging.INFO)


@router.get(
    "/health",
    status_code=status.HTTP_200_OK,
    response_model=Health,
)
def health(
    token: str = Depends(verify_token)
):
    """
    Check heath
    """
    return Health()


@router.post(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=Folder
)
async def create_upload_folder(
    token: str = Depends(verify_token),
):
    # Create a folder with a random UUID
    return create_folder()


@router.post(
    "/{folder}",
)
async def upload(
    folder: str,
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    token: str = Depends(verify_token),
):
    try:
        logging.info(f"Uploading file {file.filename} to folder {folder}")

        folder_path = settings.UPLOAD_FOLDER + folder

        file.file.seek(0, 2)
        file_size = file.file.tell()
        logging.info(f"File size: {file_size} bytes")

        # move the cursor back to the beginning
        await file.seek(0)

        if not os.path.exists(folder_path):
            raise HTTPException(
                status_code=400, detail="Folder is invalid")

        if file_size > settings.MAX_FILE_SIZE_BYTES:
            raise HTTPException(
                status_code=413, detail="File size exceeds the maximum limit"
            )

        file_extension = get_extension(file)

        if file_extension not in settings.ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=400, detail="Only CSV and Excel files are allowed")

        file_path = generate_store_path(folder_path, file_extension)

        background_tasks.add_task(save_file, file_path, file)

        return JSONResponse(
            content={"message": "File uploaded successfully"}, status_code=200)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
