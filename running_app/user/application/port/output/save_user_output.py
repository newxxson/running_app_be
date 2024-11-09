import abc

from running_app.user.domain.user import User


class SaveUserOutput(abc.ABC):
    """Save user output port."""

    @abc.abstractmethod
    async def save_user(self, user: User) -> None:
        """Save user."""
