import abc
from uuid import UUID

from running_app.running.run.domain.run import Run


class QueryRunUseCase(abc.ABC):
    """Query run use case interface."""

    @abc.abstractmethod
    async def find_run_by_run_id(self, run_identifier: UUID) -> Run | None:
        """Find run by run id."""
