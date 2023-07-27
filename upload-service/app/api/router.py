import logging
import os

from app.core.config import settings
from app.core.verify import verify_token
from app.models.schemas.files import Folder
from app.models.schemas.health import Health
from app.service.file import create_folder, save_file
from app.utils.helpers import is_upload_file_valid
from fastapi import (APIRouter, BackgroundTasks, Depends, File, Header,
                     HTTPException, UploadFile, status)
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
    x_md5_hash: str = Header(None),
    token: str = Depends(verify_token),
):
    logging.info(f"Uploading file {file.filename} to folder {folder}")

    folder_path = settings.UPLOAD_FOLDER + folder

    if not os.path.exists(folder_path):
        raise HTTPException(
            status_code=400, detail="Folder is invalid")

    if not await is_upload_file_valid(file, x_md5_hash):
        raise HTTPException(
            status_code=400, detail="Upload failed.")

    background_tasks.add_task(save_file, file, folder_path)

    return JSONResponse(
        content={"message": "File uploaded successfully"}, status_code=200)
