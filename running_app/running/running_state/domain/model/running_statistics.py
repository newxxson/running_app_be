import datetime
from uuid import UUID
from pydantic import BaseModel


class RunningStatistics(BaseModel):
    """크루 러닝 통계 도메인 오브젝트입니다."""

    run_identifier: UUID

    time: datetime.datetime

    speed: float

    latitude: float
    longitude: float
