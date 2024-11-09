import abc

from running_app.running.running_state.domain.running_state import RunningState


class SaveRunningStateOutput(abc.ABC):
    """Save running state output port."""

    @abc.abstractmethod
    async def save_running_state(self, running_state: RunningState) -> None:
        """Save running state."""
