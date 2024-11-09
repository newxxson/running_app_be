from uuid import UUID
import msgspec

from running_app.user.domain.enum.gender import Gender


class User(msgspec.Struct):
    """런닝 유저 도메인 오브젝트입니다."""

    identifier: UUID
    kakao_id: str

    phone: str

    nickname: str
    gender: Gender

    profile_image_url: str | None
