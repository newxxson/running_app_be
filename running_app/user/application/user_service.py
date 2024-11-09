from os import read
from injector import inject
from running_app.common.database.db_context import DBContext
from running_app.user.application.port.input.command.create_user_command import (
    CreateUserCommand,
)
from running_app.user.application.port.input.create_user_usecase import (
    CreateUserUseCase,
)
from running_app.user.application.port.output.find_user_output import FindUserOutput
from running_app.user.application.port.output.get_user_info_output import (
    GetUserInfoOutput,
)
from running_app.user.application.port.output.save_user_output import SaveUserOutput

from running_app.user.domain.exception.duplicate_user_exception import (
    DuplicateUserException,
)
from running_app.user.domain.user import User
from running_app.user.domain.user_factory import UserFactory


class UserService(CreateUserUseCase):
    """User service."""

    @inject
    def __init__(
        self,
        db_context: DBContext,
        find_user_output: FindUserOutput,
        save_user_output: SaveUserOutput,
        get_user_info_output: GetUserInfoOutput,
    ) -> None:
        self.db_context = db_context
        self.find_user_output = find_user_output
        self.save_user_output = save_user_output
        self.get_user_info_output = get_user_info_output

    async def create_user(self, *, create_user_command: CreateUserCommand) -> User:
        """Create user."""
        user_info = await self.get_user_info_output.get_user_info_by_kakao_token(
            kakao_token=create_user_command.kakao_auth_token
        )

        user = UserFactory.create(
            create_user_command=create_user_command, user_info=user_info
        )

        async with self.db_context.begin_transaction(read_only=False):
            existing_user = await self.find_user_output.find_user_by_kakao_id(
                kakao_id=user_info.kakao_id
            )

            if existing_user:
                raise DuplicateUserException()

            await self.save_user_output.save_user(user=user)

        return user
