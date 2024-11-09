import abc

from running_app.running.run.domain.run import Run


class SaveRunOutput(abc.ABC):
    """Save run output port."""

    @abc.abstractmethod
    async def save_run(self, run: Run) -> None:
        """Save run."""
