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
