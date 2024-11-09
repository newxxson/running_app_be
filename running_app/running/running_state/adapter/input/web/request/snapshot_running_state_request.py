import datetime
from uuid import UUID
from pydantic import BaseModel

from running_app.running.running_state.application.port.input.command.snapshot_running_status_command import (
    SnapshotRunningStateCommand,
)


class SnapshotRunningStateRequest(BaseModel):
    """런닝 상태 스냅샷 요청 모델."""

    running_goal_identifier: UUID

    latitude: float
    longitude: float
    time: datetime.datetime

    def to_command(self, request_user_identifier: UUID) -> SnapshotRunningStateCommand:
        return SnapshotRunningStateCommand(
            run_identifier=self.running_goal_identifier,
            latitude=self.latitude,
            longitude=self.longitude,
            runner_identifier=request_user_identifier,
            time=self.time,
        )
