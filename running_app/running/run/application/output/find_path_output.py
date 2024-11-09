import abc
from uuid import UUID

from running_app.path.domain.path import Path


class RunFindPathOutput(abc.ABC):
    """Run find path output port."""

    @abc.abstractmethod
    async def find_path_by_id(self, path_identifier: UUID) -> Path | None:
        """Find path by id."""
