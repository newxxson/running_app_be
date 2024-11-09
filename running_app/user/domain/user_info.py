import msgspec


class UserInfo(msgspec.Struct):
    """카카오로부터 받은 유저 정보입니다."""

    kakao_id: str
