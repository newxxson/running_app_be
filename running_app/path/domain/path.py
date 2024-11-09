import datetime
from uuid import UUID
import msgspec


class Path(msgspec.Struct):
    """런닝 경로 도메인 오브젝트입니다."""

    identifier: UUID

    name: str

    total_distance: float
    estimated_required_minute: float

    creator_identifier: UUID

    created_date: datetime.datetime
    last_modified_date: datetime.datetime
