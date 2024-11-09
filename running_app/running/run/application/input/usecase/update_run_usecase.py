import abc

from running_app.running.run.application.input.command.update_run_command import (
    UpdateRunCommand,
)
from running_app.running.run.domain.run import Run


class UpdateRunUseCase(abc.ABC):
    """Update run use case interface."""

    @abc.abstractmethod
    async def update_run(self, update_run_command: UpdateRunCommand) -> Run:
        """Update run."""
