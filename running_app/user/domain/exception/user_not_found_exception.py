from running_app.common.exception.business_exception import BusinessException


class UserNotFoundException(BusinessException):
    """유저를 찾을 수 없을 때 발생하는 예외입니다."""

    def __init__(self) -> None:
        super().__init__(status_code=404, message="User not found")
