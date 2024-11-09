from uuid import UUID
import msgspec


class CreatePathCommand(msgspec.Struct):
    """경로 생성 명령어입니다."""

    name: str
    total_distance: float

    creator_identifier: UUID
