import abc
from uuid import UUID

from running_app.running.running_state.domain.running_state import RunningState


class FindRunningStateOutput(abc.ABC):
    """런닝 상태 조회 결과 출력 포트"""

    @abc.abstractmethod
    async def find_running_state_by_run_identifier(
        self, run_identifier: UUID
    ) -> list[RunningState]:
        """런닝 상태를 조회합니다."""
