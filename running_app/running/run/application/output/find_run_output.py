import abc
from uuid import UUID

from running_app.running.run.domain.run import Run


class FindRunOutput(abc.ABC):
    """Find run output port."""

    @abc.abstractmethod
    async def find_run_by_id(self, run_identifier: UUID) -> Run | None:
        """Find run by id."""
