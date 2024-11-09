import abc
from uuid import UUID

from running_app.path.domain.coordinate import Coordinate
from running_app.path.domain.path import Path


class QueryPathOutput(abc.ABC):
    """Query path output interface."""

    @abc.abstractmethod
    async def query_path_coordinates(
        self, path_identifier: UUID, cursor_sequence: int, limit: int
    ) -> list[Coordinate]:
        """Query path coordinates."""

    @abc.abstractmethod
    async def query_path(self, cursor: UUID | None, limit: int) -> list[Path]:
        """Query path."""

    @abc.abstractmethod
    async def find_by_id(self, identifier: UUID) -> Path | None:
        """Find by id."""

    @abc.abstractmethod
    async def find_coordinate_by_path_id_and_sequence(
        self, path_identifier: UUID, sequence: int
    ) -> Coordinate | None:
        """Find coordinate by path id and sequence."""

    @abc.abstractmethod
    async def count_coordinates_by_path_id(self, path_identifier: UUID) -> int:
        """Count coordinates by path id."""
