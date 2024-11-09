from pydantic import BaseModel


class LoginRequest(BaseModel):
    """로그인 API 요청 모델"""

    kakao_auth_token: str
