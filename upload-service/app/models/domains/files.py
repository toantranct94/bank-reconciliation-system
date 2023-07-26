from pydantic import BaseModel, Field
from app.models.attributes.files import Files as FilesAttrs


class Folder(BaseModel):
    folder: str = Field(..., alias=FilesAttrs.folder)
