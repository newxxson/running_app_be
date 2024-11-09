class BusinessException(Exception):
    """비즈니스 에러를 나타내는 예외 클래스입니다."""

    def __init__(self, status_code: int, message: str, data: dict | None = None) -> None:
        self.status_code = status_code
        self.message = message
        self.data = data
