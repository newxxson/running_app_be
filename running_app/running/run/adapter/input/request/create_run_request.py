from uuid import UUID
from pydantic import BaseModel

from running_app.running.run.application.input.command.create_run_command import (
    CreateRunCommand,
)
from running_app.running.run.domain.enum.running_status import RunningStatus


class CreateRunRequest(BaseModel):
    """런닝 추가 API 요청 모델"""

    title: str
    description: str | None = None

    running_status: RunningStatus

    crew_identifier: UUID | None = None

    running_user_identifiers: list[UUID]

    path_identifier: UUID

    def to_command(self, request_user_identifier: UUID):
        return CreateRunCommand(
            title=self.title,
            description=self.description,
            running_status=self.running_status,
            user_identifier=request_user_identifier
            if not self.crew_identifier
            else None,
            crew_identifier=self.crew_identifier,
            running_user_identifiers=self.running_user_identifiers,
            path_identifier=self.path_identifier,
        )
