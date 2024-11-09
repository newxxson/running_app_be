from uuid import UUID
from running_app.common.exception.business_exception import BusinessException


class PathNotFoundException(BusinessException):
    """경로를 찾을 수 없습니다."""

    def __init__(self, path_identifier: UUID):
        super().__init__(status_code=404, message=f"Path not found: {path_identifier}")
