from uuid import UUID
import msgspec

from running_app.running.run.domain.enum.running_status import RunningStatus


class UpdateRunCommand(msgspec.Struct):
    """런닝 업데이트 커맨드입니다."""

    identifier: UUID

    title: str | None
    description: str | None

    running_status: RunningStatus | None

    user_identifier: UUID | None
    crew_identifier: UUID | None

    running_user_identifiers: list[UUID] | None

    request_user_identifier: UUID
