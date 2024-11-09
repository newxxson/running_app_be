import msgspec


class CoordinateModel(msgspec.Struct):
    """좌표 모델입니다."""

    latitude: float
    longitude: float
    sequence: int
