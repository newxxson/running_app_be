import abc
from uuid import UUID


from running_app.running.running_state.domain.model.running_statistics import (
    RunningStatistics,
)


class QueryRunningStatusUseCase(abc.ABC):
    """런닝 상태 조회 유스케이스"""

    @abc.abstractmethod
    async def query_running_states(
        self, running_identifier: UUID
    ) -> list[RunningStatistics]:
        """런닝 상태를 조회합니다."""
