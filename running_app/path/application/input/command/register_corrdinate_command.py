from uuid import UUID
import msgspec

from running_app.path.adapter.input.web.request.register_coordinate_request import (
    CoordinateModel,
)


class RegisterCoordinateCommand(msgspec.Struct):
    """좌표 등록 커맨드입니다."""

    coordinates: list[CoordinateModel]

    path_identifier: UUID
