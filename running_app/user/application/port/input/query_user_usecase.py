import abc
from uuid import UUID

from running_app.user.domain.user import User


class QueryUserUseCase(abc.ABC):
    """Query user use case interface."""

    @abc.abstractmethod
    async def find_user_by_id(self, *, user_identifier: UUID) -> User:
        """Find user by id."""
