from venv import logger
import aiohttp
from running_app.common.property.kakao import kakao_property
from running_app.user.application.port.output.get_user_info_output import (
    GetUserInfoOutput,
)
from running_app.user.domain.user_info import UserInfo


class KakaoApiRequest(GetUserInfoOutput):
    """Kakao API request."""

    async def get_user_info_by_kakao_token(self, kakao_token: str) -> UserInfo:
        """Get user info by kakao token."""
        logger.info(f"Get user info by kakao token: {kakao_token}")
        token_header = {"Authorization": f"Bearer {kakao_token}"}

        async with aiohttp.ClientSession() as session:
            async with session.get(
                kakao_property.kakao_api_url, headers=token_header
            ) as response:
                response_data = await response.json()

                if response.status != 200:
                    logger.error(
                        f"Failed to get user info from kakao API: {response_data}"
                    )
                    raise Exception("Failed to get user info from kakao API")

                return UserInfo(
                    kakao_id=response_data["id"],
                )
