from uuid import UUID
from running_app.common.exception.business_exception import BusinessException


class RunNotFoundException(BusinessException):
    """Run not found exception."""

    def __init__(self, run_identifier: UUID) -> None:
        super().__init__(
            status_code=404, message=f"Run not found. run_identifier: {run_identifier}"
        )
