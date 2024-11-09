from pydantic import BaseModel

from running_app.user.application.port.input.command.create_user_command import (
    CreateUserCommand,
)
from running_app.user.domain.enum import gender
from running_app.user.domain.enum.gender import Gender


class CreateUserRequest(BaseModel):
    """사용자 생성 API 요청 모델"""

    kakao_auth_token: str

    phone: str

    gender: str

    nickname: str

    def to_command(self) -> CreateUserCommand:
        return CreateUserCommand(
            kakao_auth_token=self.kakao_auth_token,
            nickname=self.nickname,
            gender=Gender(gender),
            profile_image_url=None,
            phone=self.phone,
        )
