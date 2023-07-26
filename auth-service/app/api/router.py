from app.models.schemas.health import Health
from app.models.schemas.token import Token
from app.service.auth import authenticate_client, generate_token
from fastapi import APIRouter, status
from fastapi.params import Depends

router = APIRouter()


@router.get(
    "/health",
    status_code=status.HTTP_200_OK,
    response_model=Health,
)
def health():
    """
    Check heath
    """
    return Health()


@router.post(
    "/token",
    status_code=status.HTTP_200_OK,
    response_model=Token
)
async def token(authorized: bool = Depends(authenticate_client)):
    """
    Generate token
    """
    return generate_token()
