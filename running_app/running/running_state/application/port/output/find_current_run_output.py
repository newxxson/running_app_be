import abc
from uuid import UUID

from running_app.running.running_state.domain.model.current_run import CurrentRun


class FindCurrentRunOutput(abc.ABC):
    """현재 진행중인 런닝을 찾는 output port 입니다."""

    @abc.abstractmethod
    async def find_current_run_by_run_id_and_user_id(
        self, run_identifier: UUID, runner_identifier: UUID
    ) -> CurrentRun | None:
        """현재 진행중인 러닝을 찾습니다."""
