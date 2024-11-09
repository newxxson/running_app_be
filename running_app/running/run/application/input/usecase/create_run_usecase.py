import abc

from running_app.running.run.application.input.command.create_run_command import (
    CreateRunCommand,
)
from running_app.running.run.domain.run import Run


class CreateRunUseCase(abc.ABC):
    """Create run use case interface."""

    @abc.abstractmethod
    async def create_run(self, create_run_command: CreateRunCommand) -> Run:
        """Create run."""
