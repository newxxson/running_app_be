from uuid import UUID
from pydantic import BaseModel

from running_app.user.domain.enum.gender import Gender


class UserResponse(BaseModel):
    """카카오 사용자 정보 조회 API 응답 모델"""

    identifier: UUID

    gender: str
    nickname: str

    profile_image: str | None

    @classmethod
    def from_domain(cls, user):
        return cls(
            identifier=user.identifier,
            nickname=user.nickname,
            gender=user.gender.value,
            profile_image=user.profile_image_url,
        )
