import abc
from uuid import UUID

from running_app.user.domain.user import User


class FindUserOutput(abc.ABC):
    """Find user output port."""

    @abc.abstractmethod
    async def find_user_by_kakao_id(self, kakao_id: str) -> User | None:
        """Find user by kakao id."""

    @abc.abstractmethod
    async def find_user_by_id(self, identifier: UUID) -> User | None:
        """Find user by id."""

    @abc.abstractmethod
    async def find_user_by_phone(self, phone: str) -> User | None:
        """Find user by phone."""
