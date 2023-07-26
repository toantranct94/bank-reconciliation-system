from pydantic import BaseModel, Field
from app.models.attributes.token import Token as TokenAttrs


class Token(BaseModel):
    token: str = Field(..., alias=TokenAttrs.token)


class Exp(BaseModel):
    exp: int = Field(..., alias=TokenAttrs.exp)
