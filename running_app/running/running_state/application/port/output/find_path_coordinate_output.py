import abc

from uuid import UUID

from running_app.path.domain.coordinate import Coordinate
from running_app.path.domain.path import Path


class RunningStateFindPathCoordinateOutput(abc.ABC):
    """경로 좌표를 찾는 output port 입니다."""

    @abc.abstractmethod
    async def find_path_coordinate_by_path_id_and_sequence(
        self, path_identifier: UUID, sequence: int
    ) -> Coordinate | None:
        """경로 좌표를 찾습니다."""

    @abc.abstractmethod
    async def count_path_coordinates_by_path_id(self, path_identifier: UUID) -> int:
        """경로 좌표의 개수를 세어 반환합니다."""
