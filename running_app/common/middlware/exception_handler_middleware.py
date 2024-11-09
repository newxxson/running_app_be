import traceback

from fastapi.responses import PlainTextResponse
from starlette.types import ASGIApp, Receive, Scope, Send

from running_app.common.log import logger


class ExceptionHandlerMiddleware:
    """에러가 발생할 경우 로그 모듈을 사용하여 한줄로 출력할 수 있도록 하는 미들웨어입니다."""

    def __init__(self, app: ASGIApp):
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send):
        """에러가 발생할 경우 로그 모듈을 사용하여 한줄로 출력할 수 있도록 합니다."""
        if scope["type"] != "http":
            return await self.app(scope, receive, send)

        try:
            await self.app(scope, receive, send)
        except Exception:
            logger.exception(str(traceback.format_exc()))
            response = PlainTextResponse(
                content="Internal Server Error", status_code=500
            )
            await response(scope, receive, send)
