import abc

from running_app.user.domain.model.auth_token import AuthPayload


class LoginUserUseCase(abc.ABC):
    """Login user use case interface."""

    @abc.abstractmethod
    async def login_user(self, *, kakao_token: str) -> AuthPayload:
        """Login user."""
