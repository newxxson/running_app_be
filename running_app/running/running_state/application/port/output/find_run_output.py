import abc
from uuid import UUID

from running_app.running.run.domain.run import Run


class RunningStateFindRunOutput(abc.ABC):
    """운동 정보를 찾는 output port 입니다."""

    @abc.abstractmethod
    async def find_run_by_run_id(self, run_identifier: UUID) -> Run | None:  # noqa: F821
        """운동 정보를 찾습니다."""
