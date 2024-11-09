from uuid import UUID
import msgspec

from running_app.path.domain.coordinate import Coordinate


class PathInfoModel(msgspec.Struct):
    """Path information model."""

    path_identifier: UUID

    coordinates: list[Coordinate]
