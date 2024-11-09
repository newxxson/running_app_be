import msgspec
from pydantic import BaseModel


class AuthPayload(BaseModel):
    """인증 페이로드입니다."""

    refresh_token: str
    access_token: str
