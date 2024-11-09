import abc

from running_app.running.running_state.domain.model.current_run import CurrentRun


class SaveCurrentRunOutput(abc.ABC):
    """현재 러닝을 저장하는 output port 입니다."""

    @abc.abstractmethod
    async def save_current_run(self, current_run: CurrentRun) -> None:
        """현재 러닝을 저장합니다."""
