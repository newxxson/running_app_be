import datetime
from uuid import UUID
import msgspec


class SnapshotRunningStateCommand(msgspec.Struct):
    """운동 상태 스냅샷 커맨드입니다."""

    run_identifier: UUID
    runner_identifier: UUID

    latitude: float
    longitude: float

    time: datetime.datetime
