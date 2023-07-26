import datetime

import jwt
from app.models.schemas.token import Token
from fastapi import HTTPException
from fastapi.params import Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from app.core.config import settings

security = HTTPBasic()

# just for test purposes
CLIENT_ID = "client_id"
CLIENT_SECRET = "client_secret"


def authenticate_client(credentials: HTTPBasicCredentials = Depends(security)):
    if credentials.username == CLIENT_ID and \
            credentials.password == CLIENT_SECRET:
        return True
    else:
        raise HTTPException(
            status_code=401, detail="Invalid client credentials")


def generate_token(ttl: int = settings.TOKEN_EXPIRATION_TIME) -> Token:
    payload = {
        "exp": datetime.datetime.utcnow() + datetime.timedelta(
            seconds=ttl),
    }
    token = {
        "token": jwt.encode(
            payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    }
    return Token(**token)
