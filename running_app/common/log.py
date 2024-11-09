

import logging

from pythonjsonlogger import jsonlogger



class CustomLogger(logging.Logger):
    """사용자 정의 로거 클래스."""

    def critical(self, msg, *args, **kwargs) -> None:  # noqa: ANN001, ANN002, ANN003
        """데이터독에 알람을 보내기 위해 prefix를 추가합니다."""
        msg = f"[CRITICAL_ERROR] {msg}"
        super().critical(msg, *args, **kwargs)


logging.setLoggerClass(CustomLogger)



logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = jsonlogger.JsonFormatter(
    "'[%(asctime)s] {%(pathname)s:%(lineno)d:%(funcName)s} %(levelname)s %(message)s %(dd.service)s %(dd.env)s %(dd.version)s %(dd.trace_id)s %(dd.span_id)s %(traceId)s",
    "%Y-%m-%d %H:%M:%S",
)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(formatter)

logger.addHandler(console_handler)
