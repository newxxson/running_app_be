from uuid import UUID
from pydantic import BaseModel


class UserResponse(BaseModel):
    """카카오 사용자 정보 조회 API 응답 모델"""

    identifier: UUID

    nickname: str

    @classmethod
    def from_domain(cls, user):
        return cls(
            identifier=user.identifier,
            nickname=user.nickname,
        )
