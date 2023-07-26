
from typing import List, Union

from pydantic import BaseSettings, validator


class Settings(BaseSettings):
    APP_NAME: str
    BACKEND_CORS_ORIGINS: List[str] = ["*"]
    API_PREFIX: str = "/api/upload"
    UPLOAD_FOLDER: str = "././uploads/"  # Make this outside of root folder
    MAX_FILE_SIZE_BYTES = 10 * 1024 * 1024  # 10 MB
    MAX_READ_CHUNK_BYTES = 100 * 1024  # 100 KB
    ALLOWED_EXTENSIONS = {"csv", "xlsx"}
    amqp_url: str = "amqp://guest:guest@rabbitmq"

    description = """
        Description
    """
    debug: bool = True

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(
        cls, v: Union[str, List[str]]
    ) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()
