import abc
from uuid import UUID

from running_app.path.application.input.query.query_path_command import SearchPathQuery
from running_app.path.domain.model.path_information_model import PathInfoModel
from running_app.path.domain.path import Path


class QueryPathUseCase(abc.ABC):
    """Query path use case interface."""

    @abc.abstractmethod
    async def query_path_coordinates(self, query: SearchPathQuery) -> PathInfoModel:
        """경로에 대해서 조회합니다."""

    @abc.abstractmethod
    async def query_path(self, cursor: UUID | None, limit: int) -> list[Path]:
        """경로에 대해서 조회합니다."""
