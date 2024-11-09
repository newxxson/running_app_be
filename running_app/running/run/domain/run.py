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
