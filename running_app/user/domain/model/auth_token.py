import msgspec


class AuthPayload(msgspec.Struct):
    """인증 페이로드입니다."""

    refresh_token: str
    access_token: str
