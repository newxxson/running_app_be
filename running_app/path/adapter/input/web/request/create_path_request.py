from uuid import UUID
from pydantic import BaseModel

from running_app.path.application.input.command.create_path_command import (
    CreatePathCommand,
)


class CreatePathRequest(BaseModel):
    """경로 생성 API 요청 모델"""

    name: str

    total_distance: float

    def to_command(self, creator_identifier: UUID) -> CreatePathCommand:
        return CreatePathCommand(
            name=self.name,
            total_distance=self.total_distance,
            creator_identifier=creator_identifier,
        )
