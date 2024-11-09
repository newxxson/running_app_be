import abc
from uuid import UUID

from running_app.path.domain.model.path_information_model import PathInfoModel


class QueryPathOutput(abc.ABC):
    """Query path output interface."""

    @abc.abstractmethod
    async def query_path(
        self, path_identifier: UUID, cursor_sequence: int
    ) -> PathInfoModel:
        """Query path."""
