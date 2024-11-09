import uuid
from running_app.user.application.port.input.command.create_user_command import (
    CreateUserCommand,
)
from running_app.user.domain.user import User
from running_app.user.domain.user_info import UserInfo


class UserFactory:
    @staticmethod
    def create(create_user_command: CreateUserCommand, user_info: UserInfo) -> User:
        """Create user."""
        return User(
            identifier=uuid.uuid4(),
            kakao_id=str(user_info.kakao_id),
            nickname=create_user_command.nickname,
            gender=create_user_command.gender,
            profile_image_url=None,
            phone=create_user_command.phone,
        )
