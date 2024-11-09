from uuid import UUID
import msgspec


class Coordinate(msgspec.Struct):
    """경로를 구성하는 좌표 도메인 오브젝트입니다."""

    identifier: UUID

    latitude: float
    longitude: float

    path_identifier: UUID

    sequence: int
