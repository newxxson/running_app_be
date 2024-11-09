from running_app.common.exception.business_exception import BusinessException


class DuplicateUserException(BusinessException):
    """Duplicate user exception."""

    def __init__(self) -> None:
        super().__init__(status_code=409, message="Duplicate user")
