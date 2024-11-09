import msgspec

from running_app.user.domain.enum.gender import Gender


class CreateUserCommand(msgspec.Struct):
    """유저 생성 커맨드입니다."""

    kakao_auth_token: str

    nickname: str
    gender: Gender

    profile_image_url: str | None
