import abc

from running_app.path.application.input.query.query_path_command import SearchPathQuery
from running_app.path.domain.model.path_information_model import PathInfoModel


class QueryPathUseCase(abc.ABC):
    """Query path use case interface."""

    @abc.abstractmethod
    async def query_path(self, query: SearchPathQuery) -> PathInfoModel:
        """경로에 대해서 조회합니다."""
