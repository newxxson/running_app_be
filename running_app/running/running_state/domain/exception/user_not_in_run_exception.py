from uuid import UUID
from running_app.common.exception.business_exception import BusinessException


class UserNotInRunException(BusinessException):
    """User not in run exception."""

    def __init__(self, user_identifier: UUID, run_identifier: UUID) -> None:
        super().__init__(
            status_code=400,
            message=f"User not in run. user_identifier: {user_identifier}, run_identifier: {run_identifier}",
        )
