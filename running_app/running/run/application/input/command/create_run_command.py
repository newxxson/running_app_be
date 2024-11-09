from uuid import UUID
import msgspec

from running_app.running.run.domain.enum.running_status import RunningStatus


class CreateRunCommand(msgspec.Struct):
    """런닝 생성 커맨드입니다."""

    title: str
    description: str | None

    running_status: RunningStatus

    user_identifier: UUID | None
    crew_identifier: UUID | None

    running_user_identifiers: list[UUID]

    path_identifier: UUID
