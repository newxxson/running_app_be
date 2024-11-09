from uuid import UUID
import msgspec

from running_app.path.domain.model.coordinate_model import CoordinateModel


class RegisterCoordinateCommand(msgspec.Struct):
    """좌표 등록 커맨드입니다."""

    coordinates: list[CoordinateModel]

    path_identifier: UUID
    request_user_identifier: UUID
