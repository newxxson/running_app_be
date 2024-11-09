import abc

from running_app.user.application.port.input.command.create_user_command import (
    CreateUserCommand,
)
from running_app.user.domain.user import User


class CreateUserUseCase(abc.ABC):
    """Create user use case interface."""

    @abc.abstractmethod
    async def create_user(self, *, create_user_command: CreateUserCommand) -> User:
        """Create user."""
