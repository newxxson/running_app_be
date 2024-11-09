import abc

from running_app.user.domain.user_info import UserInfo


class GetUserInfoOutput(abc.ABC):
    """Get user info output port."""

    @abc.abstractmethod
    async def get_user_info_by_kakao_token(self, kakao_token: str) -> UserInfo:
        """Get user info by kakao token."""
