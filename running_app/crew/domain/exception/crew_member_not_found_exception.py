from running_app.common.exception.business_exception import BusinessException


class CrewMemberNotFoundException(BusinessException):
    """크루 멤버를 찾을 수 없을 때 발생하는 예외입니다."""

    def __init__(self) -> None:
        super().__init__(status_code=404, message="Crew member not found")
