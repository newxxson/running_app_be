import datetime
from uuid import UUID
import msgspec


class RunningState(msgspec.Struct):
    """운동 상태 도메인 오브젝트입니다."""

    identifier: UUID
    run_identifier: UUID

    runner_identifier: UUID

    time: datetime.datetime

    latitude: float
    longitude: float

    speed: float
