from uuid import UUID
from pydantic import BaseModel

from running_app.running.run.application.input.command.update_run_command import (
    UpdateRunCommand,
)
from running_app.running.run.domain.enum.running_status import RunningStatus


class UpdateRunRequest(BaseModel):
    """런닝 수정 API 요청 모델"""

    title: str | None = None
    description: str | None = None

    running_status: str | None = None

    user_identifier: UUID | None = None
    crew_identifier: UUID | None = None

    running_user_identifiers: list[UUID] | None = None

    def to_command(
        self, run_identifier: UUID, request_user_identifier: UUID
    ) -> UpdateRunCommand:
        """커맨드 객체로 변환합니다."""
        return UpdateRunCommand(
            identifier=run_identifier,
            title=self.title,
            description=self.description,
            running_status=RunningStatus(self.running_status)
            if self.running_status
            else None,
            user_identifier=self.user_identifier,
            crew_identifier=self.crew_identifier,
            running_user_identifiers=self.running_user_identifiers,
            request_user_identifier=request_user_identifier,
        )
