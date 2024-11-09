import abc
from uuid import UUID

from running_app.running.run.domain.run import Run


class QueryRunUseCase(abc.ABC):
    """Query run use case interface."""

    @abc.abstractmethod
    async def find_run_by_run_id(self, run_identifier: UUID) -> Run | None:
        """Find run by run id."""

    @abc.abstractmethod
    async def find_coordinate_by_path_id_and_sequence(
        self, path_identifier: UUID, sequence: int
    ) -> Run | None:
        """Find coordinate by path id and sequence."""

    @abc.abstractmethod
    async def count_coordinates_by_path_id(self, path_identifier: UUID) -> int:
        """Count coordinates by path id."""
