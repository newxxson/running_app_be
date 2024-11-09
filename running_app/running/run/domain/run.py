import datetime
from uuid import UUID
import msgspec

from running_app.running.run.domain.enum.running_status import RunningStatus


class Run(msgspec.Struct):
    """운동 목표 도메인 오브젝트입니다."""

    identifier: UUID

    title: str
    description: str | None

    running_status: RunningStatus

    user_identifier: UUID | None
    crew_identifier: UUID | None

    running_user_identifiers: list[UUID]

    total_distance: float

    path_identifier: UUID

    created_date: datetime.datetime

    def update(
        self,
        title: str | None,
        description: str | None,
        running_status: RunningStatus | None,
        user_identifier: UUID | None,
        crew_identifier: UUID | None,
        running_user_identifiers: list[UUID] | None,
    ) -> None:
        """운동 목표 정보를 업데이트합니다."""
        if title:
            self.title = title
        if description:
            self.description = description
        if running_status:
            self.running_status = running_status
        if user_identifier:
            self.user_identifier = user_identifier
        if crew_identifier:
            self.crew_identifier = crew_identifier
        if running_user_identifiers:
            self.running_user_identifiers = running_user_identifiers
